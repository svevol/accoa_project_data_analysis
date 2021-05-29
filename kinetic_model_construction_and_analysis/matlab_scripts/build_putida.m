% Sample a kinetic model ensemble (reference point)

clearvars
rng('shuffle');																											% for reproducibility
delete(gcp('nocreate'));       				            																% check first that no other process is running
addpath(fullfile('..', 'matlab_code', 'analysisFxns'), ...
        fullfile('..', 'matlab_code', 'ensembleFxns'), ...
        fullfile('..', 'matlab_code', 'patternFxns'));

% only valid/stable models are kept, and it will keep sampling until the
%  "Number of particles" defined in the excel is reached, however, it is a
%  good idea to define the maximum number of models to be sampled in total, 
%  otherwise if no stable models are foxccxund it will go on sampling forever.
maxNumberOfSamples = 20000;   


% threshold of the jacobian's eigenvalues
eigThreshold = 10^-5;

modelID = 'putida_TCA_OP_reg_no_gth_pfba_amp_new_mets_expo_update';
%modelID = 'putida_TCA_OP_reg';
inputFile = fullfile('..', 'io', 'input_putida', modelID);
outputFile = fullfile('..', 'io','output_putida', [modelID, '.mat']);

tstartout = tic;
ensemble = buildEnsemble(inputFile, outputFile, maxNumberOfSamples, eigThreshold);
toc(tstartout)