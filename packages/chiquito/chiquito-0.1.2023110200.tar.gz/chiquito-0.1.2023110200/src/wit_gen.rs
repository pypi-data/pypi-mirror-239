use std::{collections::HashMap, fmt, hash::Hash, rc::Rc};

use crate::{
    ast::{query::Queriable, ASTExpr, Circuit, StepTypeUUID},
    field::Field,
    frontend::dsl::StepTypeWGHandler,
    util::UUID,
};

/// A struct that represents a witness generation context. It provides an interface for assigning
/// values to witness columns in a circuit.
#[derive(Debug, Default, Clone)]
pub struct StepInstance<F> {
    pub step_type_uuid: StepTypeUUID,
    pub assignments: HashMap<Queriable<F>, F>,
}

impl<F: fmt::Debug> fmt::Display for StepInstance<F> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}): ", self.step_type_uuid)?;
        for (queriable, value) in self.assignments.iter() {
            write!(f, "{:?} = {:?}, ", queriable, value)?;
        }
        Ok(())
    }
}

impl<F> StepInstance<F> {
    pub fn new(step_type_uuid: StepTypeUUID) -> StepInstance<F> {
        StepInstance {
            step_type_uuid,
            assignments: HashMap::default(),
        }
    }
}

impl<F: Eq + Hash> StepInstance<F> {
    /// Takes a `Queriable` object representing the witness column (lhs) and the value (rhs) to be
    /// assigned.
    pub fn assign(&mut self, lhs: Queriable<F>, rhs: F) {
        self.assignments.insert(lhs, rhs);
    }
}

pub type Witness<F> = Vec<StepInstance<F>>;

#[derive(Debug, Default, Clone)]
pub struct TraceWitness<F> {
    pub step_instances: Witness<F>,
}

impl<F: fmt::Debug> fmt::Display for TraceWitness<F> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        // get the decimal width based on the step_instances size, add extra one leading zero
        let decimal_width = self.step_instances.len().checked_ilog10().unwrap_or(0) + 2;
        // offset(step_uuid): assignations
        for (i, step_instance) in self.step_instances.iter().enumerate() {
            writeln!(
                f,
                "{:0>width$}{}",
                i,
                step_instance,
                width = decimal_width as usize,
            )?;
        }
        Ok(())
    }
}

#[derive(Debug)]
pub struct TraceContext<F> {
    witness: TraceWitness<F>,
    num_steps: usize,
}

impl<F: Default> TraceContext<F> {
    pub fn new(num_steps: usize) -> Self {
        Self {
            witness: TraceWitness::default(),
            num_steps,
        }
    }

    pub fn get_witness(self) -> TraceWitness<F> {
        self.witness
    }
}

impl<F> TraceContext<F> {
    pub fn add<Args, WG: Fn(&mut StepInstance<F>, Args) + 'static>(
        &mut self,
        step: &StepTypeWGHandler<F, Args, WG>,
        args: Args,
    ) {
        let mut witness = StepInstance::new(step.uuid());

        (*step.wg)(&mut witness, args);

        self.witness.step_instances.push(witness);
    }

    // This function pads the rest of the circuit with the given StepTypeWGHandler
    pub fn padding<Args, WG: Fn(&mut StepInstance<F>, Args) + 'static>(
        &mut self,
        step: &StepTypeWGHandler<F, Args, WG>,
        args_fn: impl Fn() -> Args,
    ) {
        while self.witness.step_instances.len() < self.num_steps {
            self.add(step, (args_fn)());
        }
    }
}

pub type Trace<F, TraceArgs> = dyn Fn(&mut TraceContext<F>, TraceArgs) + 'static;

pub struct TraceGenerator<F, TraceArgs> {
    trace: Rc<Trace<F, TraceArgs>>,
    num_steps: usize,
}

impl<F, TraceArgs> Clone for TraceGenerator<F, TraceArgs> {
    fn clone(&self) -> Self {
        Self {
            trace: self.trace.clone(),
            num_steps: self.num_steps,
        }
    }
}

impl<F, TraceArgs> Default for TraceGenerator<F, TraceArgs> {
    fn default() -> Self {
        Self {
            trace: Rc::new(|_, _| {}),
            num_steps: 0,
        }
    }
}

impl<F: Default, TraceArgs> TraceGenerator<F, TraceArgs> {
    pub fn new(trace: Rc<Trace<F, TraceArgs>>, num_steps: usize) -> Self {
        Self { trace, num_steps }
    }

    pub fn generate(&self, args: TraceArgs) -> TraceWitness<F> {
        let mut ctx = TraceContext::new(self.num_steps);

        (self.trace)(&mut ctx, args);

        ctx.get_witness()
    }
}

#[derive(Debug, Clone)]
pub struct AutoTraceGenerator<F> {
    auto_signals: HashMap<UUID, HashMap<Queriable<F>, ASTExpr<F>>>,
}

impl<F> Default for AutoTraceGenerator<F> {
    fn default() -> Self {
        Self {
            auto_signals: Default::default(),
        }
    }
}

impl<F: Clone, TraceArgs> From<&Circuit<F, TraceArgs>> for AutoTraceGenerator<F> {
    fn from(circuit: &Circuit<F, TraceArgs>) -> Self {
        let auto_signals = circuit
            .step_types
            .iter()
            .map(|(&uuid, step_type)| (uuid, step_type.auto_signals.clone()))
            .collect();

        Self { auto_signals }
    }
}

impl<F: Field + Eq + PartialEq + Hash + Clone> AutoTraceGenerator<F> {
    pub fn generate(&self, mut witness: TraceWitness<F>) -> TraceWitness<F> {
        for step_instance in witness.step_instances.iter_mut() {
            let uuid = step_instance.step_type_uuid;

            if let Some(auto_signals) = self.auto_signals.get(&uuid) {
                self.step_gen(auto_signals, step_instance)
            }
        }

        witness
    }

    fn step_gen(
        &self,
        auto_signals: &HashMap<Queriable<F>, ASTExpr<F>>,
        witness: &mut StepInstance<F>,
    ) {
        let mut pending = auto_signals
            .keys()
            .filter(|s| witness.assignments.get(s).is_none())
            .copied()
            .collect::<Vec<Queriable<F>>>();

        let mut pending_amount = pending.len();

        while pending_amount > 0 {
            pending = pending
                .clone()
                .into_iter()
                .filter(|s| {
                    if let Some(value) = auto_signals
                        .get(s)
                        .expect("auto definition not found")
                        .eval(&witness.assignments)
                    {
                        witness.assign(*s, value)
                    }

                    witness.assignments.get(s).is_none()
                })
                .collect::<Vec<Queriable<F>>>()
                .clone();

            // in each round at least one new signal should be assigned
            if pending.len() == pending_amount {
                panic!("cannot infer some auto signals")
            }
            pending_amount = pending.len()
        }
    }
}

pub type FixedAssignment<F> = HashMap<Queriable<F>, Vec<F>>;

/// A struct that can be used a fixed column generation context. It provides an interface for
/// assigning values to fixed columns in a circuit at the specified offset.
pub struct FixedGenContext<F> {
    assignments: FixedAssignment<F>,
    num_steps: usize,
}

impl<F: Field + Hash> FixedGenContext<F> {
    pub fn new(num_steps: usize) -> Self {
        Self {
            assignments: Default::default(),
            num_steps,
        }
    }

    /// Takes a `Queriable` object representing the fixed column (lhs) and the value (rhs) to be
    /// assigned.
    pub fn assign(&mut self, offset: usize, lhs: Queriable<F>, rhs: F) {
        if !Self::is_fixed_queriable(lhs) {
            panic!("trying to assign non-fixed signal");
        }

        if let Some(assignments) = self.assignments.get_mut(&lhs) {
            assignments[offset] = rhs;
        } else {
            let mut assignments = vec![F::ZERO; self.num_steps];
            assignments[offset] = rhs;
            self.assignments.insert(lhs, assignments);
        }
    }

    pub fn get_assignments(self) -> FixedAssignment<F> {
        self.assignments
    }

    fn is_fixed_queriable(q: Queriable<F>) -> bool {
        matches!(q, Queriable::Halo2FixedQuery(_, _) | Queriable::Fixed(_, _))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        ast::{query::Queriable, FixedSignal, ForwardSignal},
        frontend::dsl::StepTypeWGHandler,
        util::uuid,
    };
    use halo2_proofs::halo2curves::bn256::Fr;

    fn dummy_args_fn() {}

    #[test]
    fn test_padding_no_witness() {
        let mut ctx = TraceContext::new(5);
        let step = StepTypeWGHandler::new(uuid(), "dummy", |_: &mut StepInstance<i32>, _: ()| {});

        assert_eq!(ctx.witness.step_instances.len(), 0);
        ctx.padding(&step, dummy_args_fn);

        assert_eq!(ctx.witness.step_instances.len(), 5);
    }

    #[test]
    fn test_padding_partial_witness() {
        let mut ctx = TraceContext::new(5);
        let step = StepTypeWGHandler::new(uuid(), "dummy", |_: &mut StepInstance<i32>, _: ()| {});

        dummy_args_fn();
        ctx.add(&step, ());

        assert_eq!(ctx.witness.step_instances.len(), 1);
        ctx.padding(&step, dummy_args_fn);

        assert_eq!(ctx.witness.step_instances.len(), 5);
    }

    #[test]
    fn test_trace_witness_display() {
        let display = format!(
            "{}",
            TraceWitness::<i32> {
                step_instances: vec![
                    StepInstance {
                        step_type_uuid: 9,
                        assignments: HashMap::from([
                            (Queriable::Fixed(FixedSignal::new("a".into()), 0), 1),
                            (Queriable::Fixed(FixedSignal::new("b".into()), 0), 2)
                        ]),
                    },
                    StepInstance {
                        step_type_uuid: 10,
                        assignments: HashMap::from([
                            (Queriable::Fixed(FixedSignal::new("a".into()), 0), 1),
                            (Queriable::Fixed(FixedSignal::new("b".into()), 0), 2)
                        ]),
                    }
                ]
            }
        );
        println!("{}", display);
    }

    #[test]
    fn test_fixed_gen_context() {
        let mut ctx = FixedGenContext::new(3);
        let fixed_signal = FixedSignal::new("dummy".to_owned());
        let queriable = Queriable::Fixed(fixed_signal, 3);

        ctx.assign(0, queriable, Fr::from(3));
        let gt = vec![Fr::from(3), Fr::from(0), Fr::from(0)];
        assert_eq!(*ctx.get_assignments().get_mut(&queriable).unwrap(), gt);
    }

    #[test]
    fn test_fixed_gen_context_multiple() {
        let mut ctx = FixedGenContext::new(3);
        let fixed_signal = FixedSignal::new("dummy".to_owned());
        let fixed_signal2 = FixedSignal::new("dummy2".to_owned());
        let queriable = Queriable::Fixed(fixed_signal, 3);
        let queriable2 = Queriable::Fixed(fixed_signal2, 3);

        ctx.assign(0, queriable, Fr::from(3));
        ctx.assign(2, queriable2, Fr::from(3));

        let gt1 = vec![Fr::from(3), Fr::from(0), Fr::from(0)];
        let gt2 = vec![Fr::from(0), Fr::from(0), Fr::from(3)];
        let mut assignment = ctx.get_assignments();
        assert_eq!(*assignment.get_mut(&queriable).unwrap(), gt1);
        assert_eq!(*assignment.get_mut(&queriable2).unwrap(), gt2);
    }

    #[test]
    fn test_auto_trace_gen() {
        let a = Queriable::Forward(
            ForwardSignal::new_with_id(uuid(), 0, "a".to_string()),
            false,
        );
        let b = Queriable::Forward(
            ForwardSignal::new_with_id(uuid(), 0, "b".to_string()),
            false,
        );
        let c = Queriable::Forward(
            ForwardSignal::new_with_id(uuid(), 0, "c".to_string()),
            false,
        );
        let step_uuid = uuid();
        let mut witness = TraceWitness::default();
        witness.step_instances.push(StepInstance {
            step_type_uuid: step_uuid,
            assignments: HashMap::from([(a, Fr::ONE), (b, Fr::ONE)]),
        });
        witness.step_instances.push(StepInstance {
            step_type_uuid: step_uuid,
            assignments: HashMap::from([(a, Fr::ONE), (b, Fr::ONE), (c, Fr::ONE)]),
        });

        let generator = AutoTraceGenerator {
            auto_signals: HashMap::from([(step_uuid, HashMap::from([(c, a + b)]))]),
        };

        let witness = generator.generate(witness);
        assert_eq!(
            witness.step_instances[0].assignments.get(&c),
            Some(&Fr::from(2))
        );
        assert_eq!(
            witness.step_instances[1].assignments.get(&c),
            Some(&Fr::ONE)
        );
    }

    #[test]
    #[should_panic]
    fn test_auto_trace_gen_panic() {
        let a = Queriable::Forward(
            ForwardSignal::new_with_id(uuid(), 0, "a".to_string()),
            false,
        );
        let b = Queriable::Forward(
            ForwardSignal::new_with_id(uuid(), 0, "b".to_string()),
            false,
        );
        let c = Queriable::Forward(
            ForwardSignal::new_with_id(uuid(), 0, "c".to_string()),
            false,
        );
        let step_uuid = uuid();
        let mut witness = TraceWitness::default();
        witness.step_instances.push(StepInstance {
            step_type_uuid: step_uuid,
            assignments: HashMap::from([(a, Fr::ONE)]),
        });

        let generator = AutoTraceGenerator {
            auto_signals: HashMap::from([(step_uuid, HashMap::from([(c, a + b)]))]),
        };

        generator.generate(witness);
    }

    #[test]
    fn test_auto_trace_gen_dep() {
        let a = Queriable::Forward(
            ForwardSignal::new_with_id(uuid(), 0, "a".to_string()),
            false,
        );
        let b = Queriable::Forward(
            ForwardSignal::new_with_id(uuid(), 0, "b".to_string()),
            false,
        );
        let c = Queriable::Forward(
            ForwardSignal::new_with_id(uuid(), 0, "c".to_string()),
            false,
        );
        let step_uuid = uuid();
        let mut witness = TraceWitness::default();
        witness.step_instances.push(StepInstance {
            step_type_uuid: step_uuid,
            assignments: HashMap::from([(a, Fr::ONE)]),
        });
        witness.step_instances.push(StepInstance {
            step_type_uuid: step_uuid,
            assignments: HashMap::from([(a, Fr::ONE), (c, Fr::ONE)]),
        });

        let generator = AutoTraceGenerator {
            auto_signals: HashMap::from([(step_uuid, HashMap::from([(c, a + b), (b, a + 1)]))]),
        };

        let witness = generator.generate(witness);
        assert_eq!(
            witness.step_instances[0].assignments.get(&b),
            Some(&Fr::from(2))
        );
        assert_eq!(
            witness.step_instances[0].assignments.get(&c),
            Some(&Fr::from(3))
        );
        assert_eq!(
            witness.step_instances[1].assignments.get(&b),
            Some(&Fr::from(2))
        );
        assert_eq!(
            witness.step_instances[1].assignments.get(&c),
            Some(&Fr::ONE)
        );
    }
}
