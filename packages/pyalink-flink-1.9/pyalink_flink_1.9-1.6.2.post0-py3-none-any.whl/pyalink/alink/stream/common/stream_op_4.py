# -*- coding: utf-8 -*-

from ..base import StreamOperator, BaseSinkStreamOp, BaseModelStreamOp
from ...common.types.bases.model_stream_scan_params import ModelStreamScanParams



class ModelStreamFileSinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.ModelStreamFileSinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ModelStreamFileSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setNumKeepModel(self, val):
        return self._add_param('numKeepModel', val)



class ModelStreamFileSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.ModelStreamFileSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ModelStreamFileSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setScanInterval(self, val):
        return self._add_param('scanInterval', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setStartTime(self, val):
        return self._add_param('startTime', val)



class MultiHotPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.MultiHotPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultiHotPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class MultiStringIndexerPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.MultiStringIndexerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultiStringIndexerPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class MultilayerPerceptronPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.classification.MultilayerPerceptronPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultilayerPerceptronPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class NGramStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.nlp.NGramStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NGramStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setN(self, val):
        return self._add_param('n', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class NaiveBayesPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.classification.NaiveBayesPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class NaiveBayesTextPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.classification.NaiveBayesTextPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesTextPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class OcsvmModelOutlierPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.outlier.OcsvmModelOutlierPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OcsvmModelOutlierPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class OcsvmOutlier4GroupedDataStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.outlier.OcsvmOutlier4GroupedDataStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OcsvmOutlier4GroupedDataStreamOp, self).__init__(*args, **kwargs)
        pass

    def setInputMTableCol(self, val):
        return self._add_param('inputMTableCol', val)

    def setOutputMTableCol(self, val):
        return self._add_param('outputMTableCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCoef0(self, val):
        return self._add_param('coef0', val)

    def setDegree(self, val):
        return self._add_param('degree', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setKernelType(self, val):
        return self._add_param('kernelType', val)

    def setMaxOutlierNumPerGroup(self, val):
        return self._add_param('maxOutlierNumPerGroup', val)

    def setMaxOutlierRatio(self, val):
        return self._add_param('maxOutlierRatio', val)

    def setNu(self, val):
        return self._add_param('nu', val)

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



class OcsvmOutlierStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.outlier.OcsvmOutlierStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OcsvmOutlierStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCoef0(self, val):
        return self._add_param('coef0', val)

    def setDegree(self, val):
        return self._add_param('degree', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setKernelType(self, val):
        return self._add_param('kernelType', val)

    def setNu(self, val):
        return self._add_param('nu', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPrecedingRows(self, val):
        return self._add_param('precedingRows', val)

    def setPrecedingTime(self, val):
        return self._add_param('precedingTime', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class OneHotPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.OneHotPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneHotPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class OnePassClusterStreamOp(BaseModelStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.clustering.OnePassClusterStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OnePassClusterStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setModelOutputInterval(self, val):
        return self._add_param('modelOutputInterval', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class OnlineFmModelFilterStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.onlinelearning.OnlineFmModelFilterStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OnlineFmModelFilterStreamOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAccuracyThreshold(self, val):
        return self._add_param('accuracyThreshold', val)

    def setAucThreshold(self, val):
        return self._add_param('aucThreshold', val)

    def setLogLossThreshold(self, val):
        return self._add_param('logLossThreshold', val)

    def setNumEvalSamples(self, val):
        return self._add_param('numEvalSamples', val)

    def setPositiveLabelValueString(self, val):
        return self._add_param('positiveLabelValueString', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class OnlineFmTrainStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.onlinelearning.OnlineFmTrainStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OnlineFmTrainStreamOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBeta(self, val):
        return self._add_param('beta', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setLambda0(self, val):
        return self._add_param('lambda0', val)

    def setLambda1(self, val):
        return self._add_param('lambda1', val)

    def setLambda2(self, val):
        return self._add_param('lambda2', val)

    def setMiniBatchSize(self, val):
        return self._add_param('miniBatchSize', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

    def setTimeInterval(self, val):
        return self._add_param('timeInterval', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)



class OnlineLearningStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.onlinelearning.OnlineLearningStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OnlineLearningStreamOp, self).__init__(*args, **kwargs)
        pass

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBeta(self, val):
        return self._add_param('beta', val)

    def setBeta1(self, val):
        return self._add_param('beta1', val)

    def setBeta2(self, val):
        return self._add_param('beta2', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setTimeInterval(self, val):
        return self._add_param('timeInterval', val)



class OnnxModelPredictStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.onnx.OnnxModelPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OnnxModelPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setModelPath(self, val):
        return self._add_param('modelPath', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setInputNames(self, val):
        return self._add_param('inputNames', val)

    def setOutputNames(self, val):
        return self._add_param('outputNames', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)



class OverCountWindowStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.OverCountWindowStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OverCountWindowStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setLatency(self, val):
        return self._add_param('latency', val)

    def setPrecedingRows(self, val):
        return self._add_param('precedingRows', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWatermarkType(self, val):
        return self._add_param('watermarkType', val)



class OverTimeWindowStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.OverTimeWindowStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OverTimeWindowStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setLatency(self, val):
        return self._add_param('latency', val)

    def setPrecedingTime(self, val):
        return self._add_param('precedingTime', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWatermarkType(self, val):
        return self._add_param('watermarkType', val)



class ParquetSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.ParquetSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ParquetSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setPartitions(self, val):
        return self._add_param('partitions', val)



class PcaPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.PcaPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PcaPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class PipelinePredictStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.PipelinePredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PipelinePredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)



class PrintStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.utils.PrintStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PrintStreamOp, self).__init__(*args, **kwargs)
        pass

    def setMaxLimit(self, val):
        return self._add_param('maxLimit', val)

    def setRefreshInterval(self, val):
        return self._add_param('refreshInterval', val)



class ProphetPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.timeseries.ProphetPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ProphetPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setCap(self, val):
        return self._add_param('cap', val)

    def setChangePointPriorScale(self, val):
        return self._add_param('changePointPriorScale', val)

    def setChangePointRange(self, val):
        return self._add_param('changePointRange', val)

    def setChangePoints(self, val):
        return self._add_param('changePoints', val)

    def setDailySeasonality(self, val):
        return self._add_param('dailySeasonality', val)

    def setFloor(self, val):
        return self._add_param('floor', val)

    def setGrowth(self, val):
        return self._add_param('growth', val)

    def setHolidays(self, val):
        return self._add_param('holidays', val)

    def setHolidaysPriorScale(self, val):
        return self._add_param('holidaysPriorScale', val)

    def setIncludeHistory(self, val):
        return self._add_param('includeHistory', val)

    def setIntervalWidth(self, val):
        return self._add_param('intervalWidth', val)

    def setMcmcSamples(self, val):
        return self._add_param('mcmcSamples', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNChangePoint(self, val):
        return self._add_param('nChangePoint', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeasonalityMode(self, val):
        return self._add_param('seasonalityMode', val)

    def setSeasonalityPriorScale(self, val):
        return self._add_param('seasonalityPriorScale', val)

    def setStanInit(self, val):
        return self._add_param('stanInit', val)

    def setUncertaintySamples(self, val):
        return self._add_param('uncertaintySamples', val)

    def setWeeklySeasonality(self, val):
        return self._add_param('weeklySeasonality', val)

    def setYearlySeasonality(self, val):
        return self._add_param('yearlySeasonality', val)



class ProphetStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.timeseries.ProphetStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ProphetStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setCap(self, val):
        return self._add_param('cap', val)

    def setChangePointPriorScale(self, val):
        return self._add_param('changePointPriorScale', val)

    def setChangePointRange(self, val):
        return self._add_param('changePointRange', val)

    def setChangePoints(self, val):
        return self._add_param('changePoints', val)

    def setDailySeasonality(self, val):
        return self._add_param('dailySeasonality', val)

    def setFloor(self, val):
        return self._add_param('floor', val)

    def setGrowth(self, val):
        return self._add_param('growth', val)

    def setHolidays(self, val):
        return self._add_param('holidays', val)

    def setHolidaysPriorScale(self, val):
        return self._add_param('holidaysPriorScale', val)

    def setIncludeHistory(self, val):
        return self._add_param('includeHistory', val)

    def setIntervalWidth(self, val):
        return self._add_param('intervalWidth', val)

    def setMcmcSamples(self, val):
        return self._add_param('mcmcSamples', val)

    def setNChangePoint(self, val):
        return self._add_param('nChangePoint', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeasonalityMode(self, val):
        return self._add_param('seasonalityMode', val)

    def setSeasonalityPriorScale(self, val):
        return self._add_param('seasonalityPriorScale', val)

    def setStanInit(self, val):
        return self._add_param('stanInit', val)

    def setUncertaintySamples(self, val):
        return self._add_param('uncertaintySamples', val)

    def setWeeklySeasonality(self, val):
        return self._add_param('weeklySeasonality', val)

    def setYearlySeasonality(self, val):
        return self._add_param('yearlySeasonality', val)



class PyScalarFnStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.utils.PyScalarFnStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PyScalarFnStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClassObject(self, val):
        return self._add_param('classObject', val)

    def setClassObjectType(self, val):
        return self._add_param('classObjectType', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setResultType(self, val):
        return self._add_param('resultType', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setPythonEnvFilePath(self, val):
        return self._add_param('pythonEnvFilePath', val)

    def setPythonVersion(self, val):
        return self._add_param('pythonVersion', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class PySqlCmdStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.PySqlCmdStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PySqlCmdStreamOp, self).__init__(*args, **kwargs)
        pass

    def setCommand(self, val):
        return self._add_param('command', val)



class PyTableFnStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.utils.PyTableFnStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PyTableFnStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClassObject(self, val):
        return self._add_param('classObject', val)

    def setClassObjectType(self, val):
        return self._add_param('classObjectType', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setResultTypes(self, val):
        return self._add_param('resultTypes', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setPythonEnvFilePath(self, val):
        return self._add_param('pythonEnvFilePath', val)

    def setPythonVersion(self, val):
        return self._add_param('pythonVersion', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class QuantileDiscretizerPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.QuantileDiscretizerPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizerPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class QuantileStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.statistics.QuantileStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileStreamOp, self).__init__(*args, **kwargs)
        pass

    def setQuantileNum(self, val):
        return self._add_param('quantileNum', val)

    def setDalayTime(self, val):
        return self._add_param('dalayTime', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setTimeInterval(self, val):
        return self._add_param('timeInterval', val)



class RandomForestPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.classification.RandomForestPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RandomForestRegPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.regression.RandomForestRegPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RandomTableSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.RandomTableSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomTableSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setMaxRows(self, val):
        return self._add_param('maxRows', val)

    def setNumCols(self, val):
        return self._add_param('numCols', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setOutputColConfs(self, val):
        return self._add_param('outputColConfs', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setTimePerSample(self, val):
        return self._add_param('timePerSample', val)

    def setTimeZones(self, val):
        return self._add_param('timeZones', val)



class RandomVectorSourceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.source.RandomVectorSourceStreamOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomVectorSourceStreamOp, self).__init__(*args, **kwargs)
        pass

    def setMaxRows(self, val):
        return self._add_param('maxRows', val)

    def setSize(self, val):
        return self._add_param('size', val)

    def setSparsity(self, val):
        return self._add_param('sparsity', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setTimePerSample(self, val):
        return self._add_param('timePerSample', val)



class ReadAudioToTensorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.audio.ReadAudioToTensorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ReadAudioToTensorStreamOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRelativeFilePathCol(self, val):
        return self._add_param('relativeFilePathCol', val)

    def setRootFilePath(self, val):
        return self._add_param('rootFilePath', val)

    def setSampleRate(self, val):
        return self._add_param('sampleRate', val)

    def setChannelFirst(self, val):
        return self._add_param('channelFirst', val)

    def setDuration(self, val):
        return self._add_param('duration', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOffset(self, val):
        return self._add_param('offset', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ReadImageToTensorStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.image.ReadImageToTensorStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ReadImageToTensorStreamOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRelativeFilePathCol(self, val):
        return self._add_param('relativeFilePathCol', val)

    def setRootFilePath(self, val):
        return self._add_param('rootFilePath', val)

    def setChannelFirst(self, val):
        return self._add_param('channelFirst', val)

    def setImageHeight(self, val):
        return self._add_param('imageHeight', val)

    def setImageWidth(self, val):
        return self._add_param('imageWidth', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RebalanceStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.RebalanceStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RebalanceStreamOp, self).__init__(*args, **kwargs)
        pass



class RecommendationRankingStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.recommendation.RecommendationRankingStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RecommendationRankingStreamOp, self).__init__(*args, **kwargs)
        pass

    def setMTableCol(self, val):
        return self._add_param('mTableCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRankingCol(self, val):
        return self._add_param('rankingCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class RedisRowSinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.RedisRowSinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RedisRowSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setClusterMode(self, val):
        return self._add_param('clusterMode', val)

    def setDatabaseIndex(self, val):
        return self._add_param('databaseIndex', val)

    def setKeyCols(self, val):
        return self._add_param('keyCols', val)

    def setPipelineSize(self, val):
        return self._add_param('pipelineSize', val)

    def setRedisIPs(self, val):
        return self._add_param('redisIPs', val)

    def setRedisPassword(self, val):
        return self._add_param('redisPassword', val)

    def setTimeout(self, val):
        return self._add_param('timeout', val)

    def setValueCols(self, val):
        return self._add_param('valueCols', val)



class RedisStringSinkStreamOp(BaseSinkStreamOp):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sink.RedisStringSinkStreamOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RedisStringSinkStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setClusterMode(self, val):
        return self._add_param('clusterMode', val)

    def setDatabaseIndex(self, val):
        return self._add_param('databaseIndex', val)

    def setKeyCol(self, val):
        return self._add_param('keyCol', val)

    def setPipelineSize(self, val):
        return self._add_param('pipelineSize', val)

    def setRedisIPs(self, val):
        return self._add_param('redisIPs', val)

    def setRedisPassword(self, val):
        return self._add_param('redisPassword', val)

    def setTimeout(self, val):
        return self._add_param('timeout', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)



class RegexTokenizerStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.nlp.RegexTokenizerStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RegexTokenizerStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setGaps(self, val):
        return self._add_param('gaps', val)

    def setMinTokenLength(self, val):
        return self._add_param('minTokenLength', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setPattern(self, val):
        return self._add_param('pattern', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setToLowerCase(self, val):
        return self._add_param('toLowerCase', val)



class RidgeRegPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.regression.RidgeRegPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RidgeRegPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class SampleStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.dataproc.SampleStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SampleStreamOp, self).__init__(*args, **kwargs)
        pass

    def setRatio(self, val):
        return self._add_param('ratio', val)

    def setWithReplacement(self, val):
        return self._add_param('withReplacement', val)



class ScorecardPredictStreamOp(BaseModelStreamOp, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.operator.stream.finance.ScorecardPredictStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ScorecardPredictStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionScoreCol(self, val):
        return self._add_param('predictionScoreCol', val)

    def setCalculateScorePerFeature(self, val):
        return self._add_param('calculateScorePerFeature', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class SegmentStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.nlp.SegmentStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SegmentStreamOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setUserDefinedDict(self, val):
        return self._add_param('userDefinedDict', val)



class SelectStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.SelectStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SelectStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)



class SessionTimeWindowStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.feature.SessionTimeWindowStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SessionTimeWindowStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setSessionGapTime(self, val):
        return self._add_param('sessionGapTime', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setLatency(self, val):
        return self._add_param('latency', val)

    def setWatermarkType(self, val):
        return self._add_param('watermarkType', val)



class ShiftStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.timeseries.ShiftStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ShiftStreamOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setShiftNum(self, val):
        return self._add_param('shiftNum', val)



class SideOutputStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.utils.SideOutputStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SideOutputStreamOp, self).__init__(*args, **kwargs)
        pass

    def setIndex(self, val):
        return self._add_param('index', val)



class SimpleSelectStreamOp(StreamOperator):
    CLS_NAME = 'com.alibaba.alink.operator.stream.sql.SelectStreamOp$SimpleSelectStreamOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SimpleSelectStreamOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

