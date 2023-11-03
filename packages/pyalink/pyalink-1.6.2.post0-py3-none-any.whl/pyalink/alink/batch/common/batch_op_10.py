# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..mixins import WithTrainInfo, EvaluationMetricsCollector, ExtractModelInfoBatchOp, WithModelInfoBatchOp



class ToVectorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.ToVectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ToVectorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorType(self, val):
        return self._add_param('vectorType', val)



class TokenizerBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.TokenizerBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TokenizerBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TorchModelPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.pytorch.TorchModelPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TorchModelPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setModelPath(self, val):
        return self._add_param('modelPath', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TreeDepthBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.graph.TreeDepthBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TreeDepthBatchOp, self).__init__(*args, **kwargs)
        pass

    def setEdgeSourceCol(self, val):
        return self._add_param('edgeSourceCol', val)

    def setEdgeTargetCol(self, val):
        return self._add_param('edgeTargetCol', val)

    def setAsUndirectedGraph(self, val):
        return self._add_param('asUndirectedGraph', val)

    def setEdgeWeightCol(self, val):
        return self._add_param('edgeWeightCol', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)



class TreeModelEncoderBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.TreeModelEncoderBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TreeModelEncoderBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TriangleListBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.graph.TriangleListBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TriangleListBatchOp, self).__init__(*args, **kwargs)
        pass

    def setEdgeSourceCol(self, val):
        return self._add_param('edgeSourceCol', val)

    def setEdgeTargetCol(self, val):
        return self._add_param('edgeTargetCol', val)



class TripleToColumnsBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.TripleToColumnsBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TripleToColumnsBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setTripleColumnCol(self, val):
        return self._add_param('tripleColumnCol', val)

    def setTripleValueCol(self, val):
        return self._add_param('tripleValueCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setTripleRowCol(self, val):
        return self._add_param('tripleRowCol', val)



class TripleToCsvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.TripleToCsvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TripleToCsvBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setTripleColumnCol(self, val):
        return self._add_param('tripleColumnCol', val)

    def setTripleValueCol(self, val):
        return self._add_param('tripleValueCol', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setTripleRowCol(self, val):
        return self._add_param('tripleRowCol', val)



class TripleToJsonBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.TripleToJsonBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TripleToJsonBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setTripleColumnCol(self, val):
        return self._add_param('tripleColumnCol', val)

    def setTripleValueCol(self, val):
        return self._add_param('tripleValueCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setTripleRowCol(self, val):
        return self._add_param('tripleRowCol', val)



class TripleToKvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.TripleToKvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TripleToKvBatchOp, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setTripleColumnCol(self, val):
        return self._add_param('tripleColumnCol', val)

    def setTripleValueCol(self, val):
        return self._add_param('tripleValueCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setTripleRowCol(self, val):
        return self._add_param('tripleRowCol', val)



class TripleToVectorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.TripleToVectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TripleToVectorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setTripleColumnCol(self, val):
        return self._add_param('tripleColumnCol', val)

    def setTripleValueCol(self, val):
        return self._add_param('tripleValueCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setTripleRowCol(self, val):
        return self._add_param('tripleRowCol', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)



class TsvSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.TsvSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TsvSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPartitionCols(self, val):
        return self._add_param('partitionCols', val)



class TsvSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.TsvSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TsvSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setIgnoreFirstLine(self, val):
        return self._add_param('ignoreFirstLine', val)

    def setPartitions(self, val):
        return self._add_param('partitions', val)

    def setSkipBlankLine(self, val):
        return self._add_param('skipBlankLine', val)



class TypeConvertBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.TypeConvertBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TypeConvertBatchOp, self).__init__(*args, **kwargs)
        pass

    def setTargetType(self, val):
        return self._add_param('targetType', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)



class UnionAllBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.UnionAllBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UnionAllBatchOp, self).__init__(*args, **kwargs)
        pass



class UnionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.UnionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UnionBatchOp, self).__init__(*args, **kwargs)
        pass



class UserCfItemsPerUserRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfItemsPerUserRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfItemsPerUserRecommBatchOp, self).__init__(*args, **kwargs)
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



class UserCfModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class UserCfRateRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfRateRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfRateRecommBatchOp, self).__init__(*args, **kwargs)
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



class UserCfSimilarUsersRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfSimilarUsersRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfSimilarUsersRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class UserCfTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setSimilarityThreshold(self, val):
        return self._add_param('similarityThreshold', val)

    def setSimilarityType(self, val):
        return self._add_param('similarityType', val)



class UserCfUsersPerItemRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfUsersPerItemRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfUsersPerItemRecommBatchOp, self).__init__(*args, **kwargs)
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



class VectorApproxNearestNeighborPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.VectorApproxNearestNeighborPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorApproxNearestNeighborPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class VectorApproxNearestNeighborTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.VectorApproxNearestNeighborTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorApproxNearestNeighborTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setTrainType(self, val):
        return self._add_param('trainType', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setNumHashTables(self, val):
        return self._add_param('numHashTables', val)

    def setNumProjectionsPerTable(self, val):
        return self._add_param('numProjectionsPerTable', val)

    def setProjectionWidth(self, val):
        return self._add_param('projectionWidth', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setSolver(self, val):
        return self._add_param('solver', val)



class VectorAssemblerBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorAssemblerBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorAssemblerBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorBiFunctionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorBiFunctionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorBiFunctionBatchOp, self).__init__(*args, **kwargs)
        pass

    def setBiFuncName(self, val):
        return self._add_param('biFuncName', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorChiSqSelectorBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.VectorChiSqSelectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorChiSqSelectorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setFdr(self, val):
        return self._add_param('fdr', val)

    def setFpr(self, val):
        return self._add_param('fpr', val)

    def setFwe(self, val):
        return self._add_param('fwe', val)

    def setNumTopFeatures(self, val):
        return self._add_param('numTopFeatures', val)

    def setPercentile(self, val):
        return self._add_param('percentile', val)

    def setSelectorType(self, val):
        return self._add_param('selectorType', val)



class VectorChiSquareTestBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.statistics.VectorChiSquareTestBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorChiSquareTestBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)



class VectorCorrelationBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.statistics.VectorCorrelationBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorCorrelationBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMethod(self, val):
        return self._add_param('method', val)



class VectorElementwiseProductBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorElementwiseProductBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorElementwiseProductBatchOp, self).__init__(*args, **kwargs)
        pass

    def setScalingVector(self, val):
        return self._add_param('scalingVector', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorFunctionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorFunctionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorFunctionBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFuncName(self, val):
        return self._add_param('funcName', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setWithVariable(self, val):
        return self._add_param('WithVariable', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorImputerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorImputerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorImputerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class VectorImputerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorImputerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorImputerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class VectorImputerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorImputerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorImputerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setFillValue(self, val):
        return self._add_param('fillValue', val)

    def setStrategy(self, val):
        return self._add_param('strategy', val)



class VectorInteractionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorInteractionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorInteractionBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorMaxAbsScalerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMaxAbsScalerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMaxAbsScalerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class VectorMaxAbsScalerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMaxAbsScalerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMaxAbsScalerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class VectorMaxAbsScalerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMaxAbsScalerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMaxAbsScalerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)



class VectorMinMaxScalerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMinMaxScalerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMinMaxScalerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class VectorMinMaxScalerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMinMaxScalerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMinMaxScalerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class VectorMinMaxScalerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMinMaxScalerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMinMaxScalerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMax(self, val):
        return self._add_param('max', val)

    def setMin(self, val):
        return self._add_param('min', val)



class VectorNearestNeighborPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.VectorNearestNeighborPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorNearestNeighborPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class VectorNearestNeighborTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.VectorNearestNeighborTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorNearestNeighborTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setTrainType(self, val):
        return self._add_param('trainType', val)

    def setMetric(self, val):
        return self._add_param('metric', val)



class VectorNormalizeBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorNormalizeBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorNormalizeBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setP(self, val):
        return self._add_param('p', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorPolynomialExpandBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorPolynomialExpandBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorPolynomialExpandBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setDegree(self, val):
        return self._add_param('degree', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorPredict(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.common.tree.Preprocessing$VectorPredict'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorPredict, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorSizeHintBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorSizeHintBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorSizeHintBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setSize(self, val):
        return self._add_param('size', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorSliceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorSliceBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorSliceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setIndices(self, val):
        return self._add_param('indices', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorStandardScalerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorStandardScalerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorStandardScalerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class VectorStandardScalerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorStandardScalerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorStandardScalerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

