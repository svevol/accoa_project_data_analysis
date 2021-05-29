% Run MCA analysis on your model ensemble

clear      				   
addpath(fullfile('..', 'matlab_code', 'analysisFxns'), ...
        fullfile('..', 'matlab_code', 'ensembleFxns'), ...
        fullfile('..', 'matlab_code', 'patternFxns'));
    
saveMCAMatrices = 1;    % whether or not to save the MCA results for all models and not just mean values
modelID = 'putida_TCA_OP_reg_no_gth_pfba_amp_new_mets_expo_update';
outputFolder = fullfile('..', 'io','output_putida');

load(fullfile(outputFolder, [modelID, '.mat']))


% Run MCA analysis

%mcaResults = controlAnalysis(ensemble, saveMCAMatrices);

% If you have promiscuous enzymes or isoenzymes you might want to run
% controlAndResponseAnalysis instead
mcaResults = controlAndResponseAnalysis(ensemble, saveMCAMatrices);


% Save MCA results
save(fullfile(outputFolder, ['MCA_', modelID, '.mat']), 'mcaResults');
write(cell2table(ensemble.rxns(ensemble.activeRxns)), fullfile(outputFolder, [modelID, '_rxnsActive.dat']));
write(cell2table(ensemble.mets(ensemble.metsActive)), fullfile(outputFolder, [modelID, '_metsActive.dat']));
write(cell2table(mcaResults.enzNames), fullfile(outputFolder, [modelID, '_enzNames.dat']));


