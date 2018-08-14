# Point Python to the path where we have installed the bad and darc packages
import sys
sys.path.insert(0, '/Users/btvincent/git-local/darc-experiments-python')


from darc.delayed import models
from darc.designs import DARCDesign
import numpy as np
import pandas as pd
import logging
import darc
from darc.delayed import models as delayed_models
from darc.risky import models as risky_models
from darc.delayed_and_risky import models as delayed_and_risky_models
import pytest


logging.basicConfig(filename='test.log', level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')


delayed_models_list = [
    delayed_models.Hyperbolic,
    delayed_models.Exponential,
    delayed_models.ConstantSensitivity,
    delayed_models.MyersonHyperboloid,
    delayed_models.ProportionalDifference,
    delayed_models.HyperbolicNonLinearUtility
]

delayed_models_list_ME = [
    delayed_models.HyperbolicMagnitudeEffect,
    delayed_models.ExponentialMagnitudeEffect,
]

risky_models_list = [
    risky_models.Hyperbolic,
    risky_models.ProportionalDifference,
    #risky_models.ProspectTheory
]

delayed_and_risky_models_list = [
    delayed_and_risky_models.MultiplicativeHyperbolic
]

# HELPER FUNCTION -------------------------------------------------------
def simulated_experiment_trial_loop(design_thing, model):
    '''run a simulated experiment trial loop'''
    for trial in range(666):
        design = design_thing.get_next_design(model, random_choice_dimension='DB')

        if design is None:
            break
        
        design_df = darc.single_design_tuple_to_df(design)
        response = model.get_simulated_response(design_df)
        design_thing.enter_trial_design_and_response(design, response)

        model.update_beliefs(design_thing.all_data)

        logging.info(f'Trial {trial} complete')


@pytest.mark.parametrize("model", delayed_models_list)
def test_model_design_integration_delayed(model):
    '''Tests integration of model and design. Basically conducts Parameter
    Estimation'''

    design_thing = DARCDesign(max_trials=5,
                              RA=list(100*np.linspace(0.05, 0.95, 10)))

    model = models.Hyperbolic(n_particles=100) 

    # Generate some made up true parameters by sampling from the model's priors
    particles_dict = {key: model.prior[key].rvs(size=1) for key in model.parameter_names}
    model.θ_true = pd.DataFrame.from_dict(particles_dict)

    simulated_experiment_trial_loop(design_thing, model)

@pytest.mark.parametrize("model", delayed_models_list_ME)
def test_model_design_integration_delayed_ME(model):
    '''Tests integration of model and design. Basically conducts Parameter
    Estimation'''

    design_thing = DARCDesign(max_trials=5,
                                      RB=[100, 500, 1_000],
                                      RA_over_RB=np.linspace(0.05, 0.95, 19).tolist())

    model = models.Hyperbolic(n_particles=100) 

    # Generate some made up true parameters by sampling from the model's priors
    particles_dict = {key: model.prior[key].rvs(size=1) for key in model.parameter_names}
    model.θ_true = pd.DataFrame.from_dict(particles_dict)

    simulated_experiment_trial_loop(design_thing, model)


@pytest.mark.parametrize("model", risky_models_list)
def test_model_design_integration_risky(model):
    '''Tests integration of model and design. Basically conducts Parameter
    Estimation'''

    design_thing = DARCDesign(max_trials=5,
                              DA=[0], DB=[0], PA=[1], 
                              PB=[0.1, 0.25, 0.5, 0.75, 0.8, 0.9, 0.99],
                              RA=list(100*np.linspace(0.05, 0.95, 91)),
                              RB=[100])

    model = models.Hyperbolic(n_particles=100) 

    # Generate some made up true parameters by sampling from the model's priors
    particles_dict = {key: model.prior[key].rvs(size=1) for key in model.parameter_names}
    model.θ_true = pd.DataFrame.from_dict(particles_dict)

    simulated_experiment_trial_loop(design_thing, model)


@pytest.mark.parametrize("model", delayed_and_risky_models_list)
def test_model_design_integration_delayed_and_risky(model):
    '''Tests integration of model and design. Basically conducts Parameter
    Estimation'''

    design_thing = DARCDesign(max_trials=5,
                              PB=[0.1, 0.2, 0.25, 0.5, 0.75, 0.8, 0.9, 0.99])

    model = models.Hyperbolic(n_particles=100) 

    # Generate some made up true parameters by sampling from the model's priors
    particles_dict = {key: model.prior[key].rvs(size=1) for key in model.parameter_names}
    model.θ_true = pd.DataFrame.from_dict(particles_dict)

    simulated_experiment_trial_loop(design_thing, model)