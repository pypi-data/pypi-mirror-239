# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..mixins import WithTrainInfo, EvaluationMetricsCollector, ExtractModelInfoBatchOp, WithModelInfoBatchOp



class KSigmaOutlierBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.KSigmaOutlierBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KSigmaOutlierBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDirection(self, val):
        return self._add_param('direction', val)

    def setFeatureCol(self, val):
        return self._add_param('featureCol', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

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



class KdeOutlierBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.KdeOutlierBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KdeOutlierBatchOp, self).__init__(*args, **kwargs)
        pass

    def setBandwidth(self, val):
        return self._add_param('bandwidth', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setKernelType(self, val):
        return self._add_param('kernelType', val)

    def setMaxOutlierNumPerGroup(self, val):
        return self._add_param('maxOutlierNumPerGroup', val)

    def setMaxOutlierRatio(self, val):
        return self._add_param('maxOutlierRatio', val)

    def setMaxSampleNumPerGroup(self, val):
        return self._add_param('maxSampleNumPerGroup', val)

    def setNumNeighbors(self, val):
        return self._add_param('numNeighbors', val)

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



class KerasSequentialClassifierPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.KerasSequentialClassifierPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KerasSequentialClassifierPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setInferBatchSize(self, val):
        return self._add_param('inferBatchSize', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KerasSequentialClassifierTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.KerasSequentialClassifierTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KerasSequentialClassifierTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLayers(self, val):
        return self._add_param('layers', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setBestMetric(self, val):
        return self._add_param('bestMetric', val)

    def setCheckpointFilePath(self, val):
        return self._add_param('checkpointFilePath', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setOptimizer(self, val):
        return self._add_param('optimizer', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setRemoveCheckpointBeforeTraining(self, val):
        return self._add_param('removeCheckpointBeforeTraining', val)

    def setSaveBestOnly(self, val):
        return self._add_param('saveBestOnly', val)

    def setSaveCheckpointsEpochs(self, val):
        return self._add_param('saveCheckpointsEpochs', val)

    def setSaveCheckpointsSecs(self, val):
        return self._add_param('saveCheckpointsSecs', val)

    def setValidationSplit(self, val):
        return self._add_param('validationSplit', val)



class KerasSequentialRegressorPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.KerasSequentialRegressorPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KerasSequentialRegressorPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setInferBatchSize(self, val):
        return self._add_param('inferBatchSize', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KerasSequentialRegressorTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.KerasSequentialRegressorTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KerasSequentialRegressorTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLayers(self, val):
        return self._add_param('layers', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setBestMetric(self, val):
        return self._add_param('bestMetric', val)

    def setCheckpointFilePath(self, val):
        return self._add_param('checkpointFilePath', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setOptimizer(self, val):
        return self._add_param('optimizer', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setRemoveCheckpointBeforeTraining(self, val):
        return self._add_param('removeCheckpointBeforeTraining', val)

    def setSaveBestOnly(self, val):
        return self._add_param('saveBestOnly', val)

    def setSaveCheckpointsEpochs(self, val):
        return self._add_param('saveCheckpointsEpochs', val)

    def setSaveCheckpointsSecs(self, val):
        return self._add_param('saveCheckpointsSecs', val)

    def setValidationSplit(self, val):
        return self._add_param('validationSplit', val)



class KeywordsExtractionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.KeywordsExtractionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KeywordsExtractionBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setDampingFactor(self, val):
        return self._add_param('dampingFactor', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setMethod(self, val):
        return self._add_param('method', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setTopN(self, val):
        return self._add_param('topN', val)

    def setWindowSize(self, val):
        return self._add_param('windowSize', val)



class KnnPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.KnnPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KnnPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setK(self, val):
        return self._add_param('k', val)

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



class KnnTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.KnnTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KnnTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class KvToColumnsBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.KvToColumnsBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToColumnsBatchOp, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KvToCsvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.KvToCsvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToCsvBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KvToJsonBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.KvToJsonBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToJsonBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KvToTripleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.KvToTripleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToTripleBatchOp, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setTripleColumnValueSchemaStr(self, val):
        return self._add_param('tripleColumnValueSchemaStr', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KvToVectorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.KvToVectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToVectorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)



class LSTNetPreProcessBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.LSTNetTrainBatchOp$LSTNetPreProcessBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LSTNetPreProcessBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setHorizon(self, val):
        return self._add_param('horizon', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWindow(self, val):
        return self._add_param('window', val)



class LSTNetPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.LSTNetPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LSTNetPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class LSTNetTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.LSTNetTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LSTNetTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCheckpointFilePath(self, val):
        return self._add_param('checkpointFilePath', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setHorizon(self, val):
        return self._add_param('horizon', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setRemoveCheckpointBeforeTraining(self, val):
        return self._add_param('removeCheckpointBeforeTraining', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWindow(self, val):
        return self._add_param('window', val)



class LassoRegModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LassoRegModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LassoRegModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class LassoRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LassoRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LassoRegPredictBatchOp, self).__init__(*args, **kwargs)
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



class LassoRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LassoRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LassoRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class LdaModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.LdaModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LdaModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class LdaPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.LdaPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LdaPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class LdaTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.LdaTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LdaTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setTopicNum(self, val):
        return self._add_param('topicNum', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBeta(self, val):
        return self._add_param('beta', val)

    def setLearningDecay(self, val):
        return self._add_param('learningDecay', val)

    def setMethod(self, val):
        return self._add_param('method', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setOnlineLearningOffset(self, val):
        return self._add_param('onlineLearningOffset', val)

    def setOptimizeDocConcentration(self, val):
        return self._add_param('optimizeDocConcentration', val)

    def setRandomSeed(self, val):
        return self._add_param('randomSeed', val)

    def setSubsamplingRate(self, val):
        return self._add_param('subsamplingRate', val)

    def setVocabSize(self, val):
        return self._add_param('vocabSize', val)



class LeaveKObjectOutBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.LeaveKObjectOutBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LeaveKObjectOutBatchOp, self).__init__(*args, **kwargs)
        pass

    def setGroupCol(self, val):
        return self._add_param('groupCol', val)

    def setObjectCol(self, val):
        return self._add_param('objectCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setFraction(self, val):
        return self._add_param('fraction', val)

    def setK(self, val):
        return self._add_param('k', val)



class LeaveTopKObjectOutBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.LeaveTopKObjectOutBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LeaveTopKObjectOutBatchOp, self).__init__(*args, **kwargs)
        pass

    def setGroupCol(self, val):
        return self._add_param('groupCol', val)

    def setObjectCol(self, val):
        return self._add_param('objectCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setFraction(self, val):
        return self._add_param('fraction', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setRateThreshold(self, val):
        return self._add_param('rateThreshold', val)



class LeftOuterJoinBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.LeftOuterJoinBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LeftOuterJoinBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJoinPredicate(self, val):
        return self._add_param('joinPredicate', val)

    def setSelectClause(self, val):
        return self._add_param('selectClause', val)

    def setType(self, val):
        return self._add_param('type', val)



class LibSvmSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.LibSvmSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LibSvmSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPartitionCols(self, val):
        return self._add_param('partitionCols', val)

    def setStartIndex(self, val):
        return self._add_param('startIndex', val)



class LibSvmSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.LibSvmSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LibSvmSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setPartitions(self, val):
        return self._add_param('partitions', val)

    def setStartIndex(self, val):
        return self._add_param('startIndex', val)



class LineBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.graph.LineBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LineBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSourceCol(self, val):
        return self._add_param('sourceCol', val)

    def setTargetCol(self, val):
        return self._add_param('targetCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setIsToUndigraph(self, val):
        return self._add_param('isToUndigraph', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setMinRhoRate(self, val):
        return self._add_param('minRhoRate', val)

    def setNegative(self, val):
        return self._add_param('negative', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOrder(self, val):
        return self._add_param('order', val)

    def setRho(self, val):
        return self._add_param('rho', val)

    def setSampleRatioPerPartition(self, val):
        return self._add_param('sampleRatioPerPartition', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class LinearRegModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearRegModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class LinearRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegPredictBatchOp, self).__init__(*args, **kwargs)
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



class LinearRegStepwisePredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearRegStepwisePredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegStepwisePredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class LinearRegStepwiseTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearRegStepwiseTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegStepwiseTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setMethod(self, val):
        return self._add_param('method', val)



class LinearRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class LinearRegWithSummaryResult(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearRegWithSummaryResult'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegWithSummaryResult, self).__init__(*args, **kwargs)
        pass



class LinearSvmModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LinearSvmModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvmModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class LinearSvmPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LinearSvmPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvmPredictBatchOp, self).__init__(*args, **kwargs)
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



class LinearSvmTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LinearSvmTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvmTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class LinearSvrPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearSvrPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvrPredictBatchOp, self).__init__(*args, **kwargs)
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



class LinearSvrTrainBatchOp(BatchOperator, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearSvrTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvrTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setC(self, val):
        return self._add_param('C', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setTau(self, val):
        return self._add_param('tau', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class LofOutlierBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.LofOutlierBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LofOutlierBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setMaxOutlierNumPerGroup(self, val):
        return self._add_param('maxOutlierNumPerGroup', val)

    def setMaxOutlierRatio(self, val):
        return self._add_param('maxOutlierRatio', val)

    def setMaxSampleNumPerGroup(self, val):
        return self._add_param('maxSampleNumPerGroup', val)

    def setNumNeighbors(self, val):
        return self._add_param('numNeighbors', val)

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



class LogisticRegressionModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LogisticRegressionModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LogisticRegressionModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class LogisticRegressionPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LogisticRegressionPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LogisticRegressionPredictBatchOp, self).__init__(*args, **kwargs)
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



class LogisticRegressionTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LogisticRegressionTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LogisticRegressionTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class LookupBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.LookupBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LookupBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMapKeyCols(self, val):
        return self._add_param('mapKeyCols', val)

    def setMapValueCols(self, val):
        return self._add_param('mapValueCols', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamUpdateMethod(self, val):
        return self._add_param('modelStreamUpdateMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class LookupHBaseBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.LookupHBaseBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LookupHBaseBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFamilyName(self, val):
        return self._add_param('familyName', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setRowKeyCols(self, val):
        return self._add_param('rowKeyCols', val)

    def setTableName(self, val):
        return self._add_param('tableName', val)

    def setZookeeperQuorum(self, val):
        return self._add_param('zookeeperQuorum', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTimeout(self, val):
        return self._add_param('timeout', val)



class LookupRecentDaysBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.LookupRecentDaysBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LookupRecentDaysBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setFeatureSchemaStr(self, val):
        return self._add_param('featureSchemaStr', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamUpdateMethod(self, val):
        return self._add_param('modelStreamUpdateMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class LookupRedisRowBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.LookupRedisRowBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LookupRedisRowBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setClusterMode(self, val):
        return self._add_param('clusterMode', val)

    def setDatabaseIndex(self, val):
        return self._add_param('databaseIndex', val)

    def setPipelineSize(self, val):
        return self._add_param('pipelineSize', val)

    def setRedisIPs(self, val):
        return self._add_param('redisIPs', val)

    def setRedisPassword(self, val):
        return self._add_param('redisPassword', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTimeout(self, val):
        return self._add_param('timeout', val)



class LookupRedisStringBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.LookupRedisStringBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LookupRedisStringBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setClusterMode(self, val):
        return self._add_param('clusterMode', val)

    def setDatabaseIndex(self, val):
        return self._add_param('databaseIndex', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setPipelineSize(self, val):
        return self._add_param('pipelineSize', val)

    def setRedisIPs(self, val):
        return self._add_param('redisIPs', val)

    def setRedisPassword(self, val):
        return self._add_param('redisPassword', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTimeout(self, val):
        return self._add_param('timeout', val)



class LookupValueInTimeSeriesBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.LookupValueInTimeSeriesBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LookupValueInTimeSeriesBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setTimeSeriesCol(self, val):
        return self._add_param('timeSeriesCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

