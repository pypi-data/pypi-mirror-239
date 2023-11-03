# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..mixins import WithTrainInfo, EvaluationMetricsCollector, ExtractModelInfoBatchOp, WithModelInfoBatchOp



class FmClassifierModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.FmClassifierModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmClassifierModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class FmClassifierPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.FmClassifierPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmClassifierPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class FmClassifierTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.FmClassifierTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmClassifierTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setInitStdev(self, val):
        return self._add_param('initStdev', val)

    def setLambda0(self, val):
        return self._add_param('lambda0', val)

    def setLambda1(self, val):
        return self._add_param('lambda1', val)

    def setLambda2(self, val):
        return self._add_param('lambda2', val)

    def setLearnRate(self, val):
        return self._add_param('learnRate', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)



class FmItemsPerUserRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FmItemsPerUserRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmItemsPerUserRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setExcludeKnown(self, val):
        return self._add_param('excludeKnown', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class FmPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.common.fm.FmPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class FmRateRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FmRateRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRateRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class FmRecommBinaryImplicitTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FmRecommBinaryImplicitTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRecommBinaryImplicitTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setInitStdev(self, val):
        return self._add_param('initStdev', val)

    def setItemCategoricalFeatureCols(self, val):
        return self._add_param('itemCategoricalFeatureCols', val)

    def setItemFeatureCols(self, val):
        return self._add_param('itemFeatureCols', val)

    def setLambda0(self, val):
        return self._add_param('lambda0', val)

    def setLambda1(self, val):
        return self._add_param('lambda1', val)

    def setLambda2(self, val):
        return self._add_param('lambda2', val)

    def setLearnRate(self, val):
        return self._add_param('learnRate', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setUserCategoricalFeatureCols(self, val):
        return self._add_param('userCategoricalFeatureCols', val)

    def setUserFeatureCols(self, val):
        return self._add_param('userFeatureCols', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)



class FmRecommTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FmRecommTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRecommTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setInitStdev(self, val):
        return self._add_param('initStdev', val)

    def setItemCategoricalFeatureCols(self, val):
        return self._add_param('itemCategoricalFeatureCols', val)

    def setItemFeatureCols(self, val):
        return self._add_param('itemFeatureCols', val)

    def setLambda0(self, val):
        return self._add_param('lambda0', val)

    def setLambda1(self, val):
        return self._add_param('lambda1', val)

    def setLambda2(self, val):
        return self._add_param('lambda2', val)

    def setLearnRate(self, val):
        return self._add_param('learnRate', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

    def setUserCategoricalFeatureCols(self, val):
        return self._add_param('userCategoricalFeatureCols', val)

    def setUserFeatureCols(self, val):
        return self._add_param('userFeatureCols', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)



class FmRegressorModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.FmRegressorModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRegressorModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class FmRegressorPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.FmRegressorPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRegressorPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class FmRegressorTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.FmRegressorTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRegressorTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setInitStdev(self, val):
        return self._add_param('initStdev', val)

    def setLambda0(self, val):
        return self._add_param('lambda0', val)

    def setLambda1(self, val):
        return self._add_param('lambda1', val)

    def setLambda2(self, val):
        return self._add_param('lambda2', val)

    def setLearnRate(self, val):
        return self._add_param('learnRate', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)



class FmUsersPerItemRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FmUsersPerItemRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmUsersPerItemRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setExcludeKnown(self, val):
        return self._add_param('excludeKnown', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class FpGrowthBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.associationrule.FpGrowthBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FpGrowthBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemsCol(self, val):
        return self._add_param('itemsCol', val)

    def setMaxConsequentLength(self, val):
        return self._add_param('maxConsequentLength', val)

    def setMaxPatternLength(self, val):
        return self._add_param('maxPatternLength', val)

    def setMinConfidence(self, val):
        return self._add_param('minConfidence', val)

    def setMinLift(self, val):
        return self._add_param('minLift', val)

    def setMinSupportCount(self, val):
        return self._add_param('minSupportCount', val)

    def setMinSupportPercent(self, val):
        return self._add_param('minSupportPercent', val)



class FullOuterJoinBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.FullOuterJoinBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FullOuterJoinBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJoinPredicate(self, val):
        return self._add_param('joinPredicate', val)

    def setSelectClause(self, val):
        return self._add_param('selectClause', val)

    def setType(self, val):
        return self._add_param('type', val)



class GbdtEncoderPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.GbdtEncoderPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtEncoderPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class GbdtEncoderTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.GbdtEncoderTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtEncoderTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAlgoType(self, val):
        return self._add_param('algoType', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCriteria(self, val):
        return self._add_param('criteria', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setFeatureImportanceType(self, val):
        return self._add_param('featureImportanceType', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setNewtonStep(self, val):
        return self._add_param('newtonStep', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setSketchEps(self, val):
        return self._add_param('sketchEps', val)

    def setSketchRatio(self, val):
        return self._add_param('sketchRatio', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setUseEpsilonApproQuantile(self, val):
        return self._add_param('useEpsilonApproQuantile', val)

    def setUseMissing(self, val):
        return self._add_param('useMissing', val)

    def setUseOneHot(self, val):
        return self._add_param('useOneHot', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class GbdtModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.GbdtModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class GbdtPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.GbdtPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class GbdtRegEncoderTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.GbdtRegEncoderTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegEncoderTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAlgoType(self, val):
        return self._add_param('algoType', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCriteria(self, val):
        return self._add_param('criteria', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setFeatureImportanceType(self, val):
        return self._add_param('featureImportanceType', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setNewtonStep(self, val):
        return self._add_param('newtonStep', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setSketchEps(self, val):
        return self._add_param('sketchEps', val)

    def setSketchRatio(self, val):
        return self._add_param('sketchRatio', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setUseEpsilonApproQuantile(self, val):
        return self._add_param('useEpsilonApproQuantile', val)

    def setUseMissing(self, val):
        return self._add_param('useMissing', val)

    def setUseOneHot(self, val):
        return self._add_param('useOneHot', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class GbdtRegModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GbdtRegModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class GbdtRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GbdtRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class GbdtRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GbdtRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAlgoType(self, val):
        return self._add_param('algoType', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCriteria(self, val):
        return self._add_param('criteria', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setFeatureImportanceType(self, val):
        return self._add_param('featureImportanceType', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setNewtonStep(self, val):
        return self._add_param('newtonStep', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setSketchEps(self, val):
        return self._add_param('sketchEps', val)

    def setSketchRatio(self, val):
        return self._add_param('sketchRatio', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setUseEpsilonApproQuantile(self, val):
        return self._add_param('useEpsilonApproQuantile', val)

    def setUseMissing(self, val):
        return self._add_param('useMissing', val)

    def setUseOneHot(self, val):
        return self._add_param('useOneHot', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class GbdtTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.GbdtTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAlgoType(self, val):
        return self._add_param('algoType', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCriteria(self, val):
        return self._add_param('criteria', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setFeatureImportanceType(self, val):
        return self._add_param('featureImportanceType', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setNewtonStep(self, val):
        return self._add_param('newtonStep', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setSketchEps(self, val):
        return self._add_param('sketchEps', val)

    def setSketchRatio(self, val):
        return self._add_param('sketchRatio', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setUseEpsilonApproQuantile(self, val):
        return self._add_param('useEpsilonApproQuantile', val)

    def setUseMissing(self, val):
        return self._add_param('useMissing', val)

    def setUseOneHot(self, val):
        return self._add_param('useOneHot', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class GenerateFeatureOfLatestBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.GenerateFeatureOfLatestBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GenerateFeatureOfLatestBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureDefinitions(self, val):
        return self._add_param('featureDefinitions', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)



class GenerateFeatureOfLatestNDaysBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.GenerateFeatureOfLatestNDaysBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GenerateFeatureOfLatestNDaysBatchOp, self).__init__(*args, **kwargs)
        pass

    def setBaseDate(self, val):
        return self._add_param('baseDate', val)

    def setFeatureDefinitions(self, val):
        return self._add_param('featureDefinitions', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setExtendFeatures(self, val):
        return self._add_param('extendFeatures', val)



class GenerateFeatureOfWindowBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.GenerateFeatureOfWindowBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GenerateFeatureOfWindowBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureDefinitions(self, val):
        return self._add_param('featureDefinitions', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)



class GeoKMeansPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GeoKMeansPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GeoKMeansPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setPredictionDistanceCol(self, val):
        return self._add_param('predictionDistanceCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class GeoKMeansTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GeoKMeansTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GeoKMeansTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLatitudeCol(self, val):
        return self._add_param('latitudeCol', val)

    def setLongitudeCol(self, val):
        return self._add_param('longitudeCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setInitMode(self, val):
        return self._add_param('initMode', val)

    def setInitSteps(self, val):
        return self._add_param('initSteps', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setRandomSeed(self, val):
        return self._add_param('randomSeed', val)



class GlmEvaluationBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GlmEvaluationBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmEvaluationBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFamily(self, val):
        return self._add_param('family', val)

    def setFitIntercept(self, val):
        return self._add_param('fitIntercept', val)

    def setLink(self, val):
        return self._add_param('link', val)

    def setLinkPower(self, val):
        return self._add_param('linkPower', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOffsetCol(self, val):
        return self._add_param('offsetCol', val)

    def setRegParam(self, val):
        return self._add_param('regParam', val)

    def setVariancePower(self, val):
        return self._add_param('variancePower', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class GlmModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GlmModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class GlmPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GlmPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLinkPredResultCol(self, val):
        return self._add_param('linkPredResultCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class GlmTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GlmTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFamily(self, val):
        return self._add_param('family', val)

    def setFitIntercept(self, val):
        return self._add_param('fitIntercept', val)

    def setLink(self, val):
        return self._add_param('link', val)

    def setLinkPower(self, val):
        return self._add_param('linkPower', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOffsetCol(self, val):
        return self._add_param('offsetCol', val)

    def setRegParam(self, val):
        return self._add_param('regParam', val)

    def setVariancePower(self, val):
        return self._add_param('variancePower', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class GmmModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GmmModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GmmModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class GmmPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GmmPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GmmPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class GmmTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GmmTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GmmTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setRandomSeed(self, val):
        return self._add_param('randomSeed', val)



class GroupByBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.GroupByBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GroupByBatchOp, self).__init__(*args, **kwargs)
        pass

    def setGroupByPredicate(self, val):
        return self._add_param('groupByPredicate', val)

    def setSelectClause(self, val):
        return self._add_param('selectClause', val)



class GroupDbscanBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GroupDbscanBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GroupDbscanBatchOp, self).__init__(*args, **kwargs)
        pass

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setMinPoints(self, val):
        return self._add_param('minPoints', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setGroupMaxSamples(self, val):
        return self._add_param('groupMaxSamples', val)

    def setIsOutputVector(self, val):
        return self._add_param('isOutputVector', val)

    def setSkip(self, val):
        return self._add_param('skip', val)



class GroupDbscanModelBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GroupDbscanModelBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GroupDbscanModelBatchOp, self).__init__(*args, **kwargs)
        pass

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setMinPoints(self, val):
        return self._add_param('minPoints', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setGroupMaxSamples(self, val):
        return self._add_param('groupMaxSamples', val)

    def setSkip(self, val):
        return self._add_param('skip', val)



class GroupEmBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GroupEmBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GroupEmBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)



class GroupGeoDbscanBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GroupGeoDbscanBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GroupGeoDbscanBatchOp, self).__init__(*args, **kwargs)
        pass

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setLatitudeCol(self, val):
        return self._add_param('latitudeCol', val)

    def setLongitudeCol(self, val):
        return self._add_param('longitudeCol', val)

    def setMinPoints(self, val):
        return self._add_param('minPoints', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setGroupMaxSamples(self, val):
        return self._add_param('groupMaxSamples', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSkip(self, val):
        return self._add_param('skip', val)



class GroupGeoDbscanModelBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GroupGeoDbscanModelBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GroupGeoDbscanModelBatchOp, self).__init__(*args, **kwargs)
        pass

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setLatitudeCol(self, val):
        return self._add_param('latitudeCol', val)

    def setLongitudeCol(self, val):
        return self._add_param('longitudeCol', val)

    def setMinPoints(self, val):
        return self._add_param('minPoints', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setGroupMaxSamples(self, val):
        return self._add_param('groupMaxSamples', val)

    def setSkip(self, val):
        return self._add_param('skip', val)



class GroupKMeansBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GroupKMeansBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GroupKMeansBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)



class GroupScorecardPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.finance.GroupScorecardPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GroupScorecardPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionScoreCol(self, val):
        return self._add_param('predictionScoreCol', val)

    def setCalculateScorePerFeature(self, val):
        return self._add_param('calculateScorePerFeature', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class GroupScorecardTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.finance.GroupScorecardTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GroupScorecardTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setAlphaEntry(self, val):
        return self._add_param('alphaEntry', val)

    def setAlphaStay(self, val):
        return self._add_param('alphaStay', val)

    def setConstOptimMethod(self, val):
        return self._add_param('constOptimMethod', val)

    def setDefaultWoe(self, val):
        return self._add_param('defaultWoe', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setForceSelectedCols(self, val):
        return self._add_param('forceSelectedCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setLinearModelType(self, val):
        return self._add_param('linearModelType', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinOutcomeSamplesPerLeaf(self, val):
        return self._add_param('minOutcomeSamplesPerLeaf', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setOdds(self, val):
        return self._add_param('odds', val)

    def setPdo(self, val):
        return self._add_param('pdo', val)

    def setPositiveLabelValueString(self, val):
        return self._add_param('positiveLabelValueString', val)

    def setScaleInfo(self, val):
        return self._add_param('scaleInfo', val)

    def setScaledValue(self, val):
        return self._add_param('scaledValue', val)

    def setTreeSplitMeasure(self, val):
        return self._add_param('treeSplitMeasure', val)

    def setVizName(self, val):
        return self._add_param('vizName', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithSelector(self, val):
        return self._add_param('withSelector', val)



class GroupedFpGrowthBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.associationrule.GroupedFpGrowthBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GroupedFpGrowthBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemsCol(self, val):
        return self._add_param('itemsCol', val)

    def setGroupCol(self, val):
        return self._add_param('groupCol', val)

    def setMaxConsequentLength(self, val):
        return self._add_param('maxConsequentLength', val)

    def setMaxPatternLength(self, val):
        return self._add_param('maxPatternLength', val)

    def setMinConfidence(self, val):
        return self._add_param('minConfidence', val)

    def setMinLift(self, val):
        return self._add_param('minLift', val)

    def setMinSupportCount(self, val):
        return self._add_param('minSupportCount', val)

    def setMinSupportPercent(self, val):
        return self._add_param('minSupportPercent', val)



class HBaseSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.HBaseSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(HBaseSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFamilyName(self, val):
        return self._add_param('familyName', val)

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setRowKeyCols(self, val):
        return self._add_param('rowKeyCols', val)

    def setTableName(self, val):
        return self._add_param('tableName', val)

    def setZookeeperQuorum(self, val):
        return self._add_param('zookeeperQuorum', val)

    def setTimeout(self, val):
        return self._add_param('timeout', val)

    def setValueCols(self, val):
        return self._add_param('valueCols', val)



class HashCrossFeatureBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.HashCrossFeatureBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(HashCrossFeatureBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setNumFeatures(self, val):
        return self._add_param('numFeatures', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class HbosOutlier4GroupedDataBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.HbosOutlier4GroupedDataBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(HbosOutlier4GroupedDataBatchOp, self).__init__(*args, **kwargs)
        pass

    def setInputMTableCol(self, val):
        return self._add_param('inputMTableCol', val)

    def setOutputMTableCol(self, val):
        return self._add_param('outputMTableCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxOutlierNumPerGroup(self, val):
        return self._add_param('maxOutlierNumPerGroup', val)

    def setMaxOutlierRatio(self, val):
        return self._add_param('maxOutlierRatio', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class HbosOutlierBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.HbosOutlierBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(HbosOutlierBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxOutlierNumPerGroup(self, val):
        return self._add_param('maxOutlierNumPerGroup', val)

    def setMaxOutlierRatio(self, val):
        return self._add_param('maxOutlierRatio', val)

    def setMaxSampleNumPerGroup(self, val):
        return self._add_param('maxSampleNumPerGroup', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class HoltWintersBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.HoltWintersBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(HoltWintersBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBeta(self, val):
        return self._add_param('beta', val)

    def setDoSeasonal(self, val):
        return self._add_param('doSeasonal', val)

    def setDoTrend(self, val):
        return self._add_param('doTrend', val)

    def setFrequency(self, val):
        return self._add_param('frequency', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setLevelStart(self, val):
        return self._add_param('levelStart', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeasonalStart(self, val):
        return self._add_param('seasonalStart', val)

    def setSeasonalType(self, val):
        return self._add_param('seasonalType', val)

    def setTrendStart(self, val):
        return self._add_param('trendStart', val)

