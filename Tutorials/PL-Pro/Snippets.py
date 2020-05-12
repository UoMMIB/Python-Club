from sklearn import tree
import graphviz
from sklearn.model_selection import train_test_split



x_train,x_test, y_train, y_test = train_test_split(pyhyschem_descriptors.loc[:,['LogP',
                                                                          'NumAromaticRings']],
                                                   data_for_model['activity'],
                                                   test_size=0.2)

tree_data = tree.export_graphviz(classifier,
                                 out_file = None,
                                 feature_names = ['LogP','NumAromaticRings'],
                                class_names=['Miss','Hit'],
                                rotate=True)
graph = graphviz.Source(tree_data)

from sklearn.metrics import roc_curve, roc_auc_score

def PlotModelEvaluation(predictions, ytest, ModelTitle):
    confusion_matrix = pd.crosstab(predictions, ytest)
    plt.figure(figsize=(5,5))
    plt.title(f'{ModelTitle} Confusion Matrix')
    sns.heatmap(confusion_matrix, annot=True)
    plt.ylabel('predicted')
    plt.show()


    plt.figure(figsize = (7,5))
    false_positive_rate, true_positive_rate, thresholds = roc_curve(ytest, predictions)
    plt.plot(false_positive_rate, true_positive_rate)
    roc_auc = roc_auc_score(ytest, predictions)
    plt.title(f'{ModelTitle} ROC Curve, AUC = {round(roc_auc,3)}')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positve Rate')
    plt.show()


def Pipeline(data, modelName):
    sample = UnderSample(data)

    rdkit_Fragments = pd.DataFrame(compounds_of_interest['smiles'].apply(RDKitBagOfFeatures).to_list())
    our_Fragments = pd.DataFrame(data_for_model['smiles'].apply(SubstructureMatch, args = [hand_crafted_features]).to_list())
    pyhyschem_descriptors = pd.DataFrame(data_for_model['smiles'].apply(PhysChemFeatures).to_list())

    x = pd.concat(objs = [rdkit_Fragments, our_Fragments, pyhyschem_descriptors],
                             axis = 1,
                             join = 'inner')
    y = data_for_model['activity']

    x_train,x_test, y_train, y_test = train_test_split(x,
                                                   y,
                                                   test_size=0.2)

    adaboost = AdaBoostClassifier(base_estimator=tree.DecisionTreeClassifier(),
                             n_estimators=500)

    adaboost.fit(x_train, y_train)

    predictions_adaboost = adaboost.predict(x_test)

    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, predictions)

    roc_auc = roc_auc_score(y_test, predictions)

    output_dict = {'name':modelName,
                  'model':adaboost,
                  'roc_auc':roc_auc}

    return output_dict


from sklearn.model_selection import cross_validate
from sklearn.metrics import  make_scorer

estimator = cross_validate(tree.DecisionTreeClassifier(),
                           features_scaled, data_for_model['activity'],
                           cv=20,
                           return_estimator=True,
                          scoring = make_scorer(roc_auc_score))


print(f"Mean test score (ROC-AUC): {estimator['test_score'].mean()}\n\n")

feature_importances = pd.DataFrame([i.feature_importances_ for i in estimator['estimator']],
                                  columns = features_scaled.columns)
feature_importances.mean(axis=0).nlargest(10)


from sklearn.ensemble import AdaBoostClassifier

adaboost = AdaBoostClassifier(base_estimator=tree.DecisionTreeClassifier(),
                             n_estimators=500)

ft_importances = pd.Series(rf.feature_importances_, index = features_scaled.columns)
important_features = ft_importances.loc[ft_importances>0]

plt.figure(figsize = (5,20))
plt.title('Important Features')
plt.barh(important_features.index, important_features)
plt.xlabel('Relative Feature Importance')
plt.show()





drug_repurposingLib = pd.read_csv('coronavirus_data/data/broad_repurposing_library.csv')
drug_repurposingLib['scaffolds'] = drug_repurposingLib['smiles'].apply(MurckoScaffold.MurckoScaffoldSmilesFromSmiles)


repurposed_of_interest = drug_repurposingLib.loc[drug_repurposingLib['scaffolds'].isin(tmp['scaffold smiles']),:]
repurposed_of_interest.reset_index(inplace=True)

Repurposed_rdkitFragments = pd.DataFrame(repurposed_of_interest['smiles'].apply(RDKitBagOfFeatures).to_list())
Repurposed_our_Fragments = pd.DataFrame(repurposed_of_interest['smiles'].apply(SubstructureMatch, args = [hand_crafted_features]).to_list())
Repurposed_pyhyschem_descriptors = pd.DataFrame(repurposed_of_interest['smiles'].apply(PhysChemFeatures).to_list())

repurposed_of_interest_features = pd.concat([Repurposed_rdkitFragments, Repurposed_our_Fragments, Repurposed_pyhyschem_descriptors],
                         axis = 1,
                         join = 'inner')



PandasTools.AddMoleculeColumnToFrame(repurposed_of_interest, smilesCol = 'smiles', molCol = 'Mol')
repurposed_of_interest


predictions_on_repurposed_compounds = pd.DataFrame(rf.predict_proba(repurposed_of_interest_features_scaled))
predictions_on_repurposed_compounds.columns = ['Prob miss','Prob hit']
predictions_with_structures = pd.concat([repurposed_of_interest,predictions_on_repurposed_compounds], axis=1, join = 'inner')

PandasTools.AddMoleculeColumnToFrame(predictions_with_structures, smilesCol = 'smiles', molCol = 'Mol')
predictions_with_structures.sort_values('Prob hit',ascending=False)[['Mol','Prob hit']]
