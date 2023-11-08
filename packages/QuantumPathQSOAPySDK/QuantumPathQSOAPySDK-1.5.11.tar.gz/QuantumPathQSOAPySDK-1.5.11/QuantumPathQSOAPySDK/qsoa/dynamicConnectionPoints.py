from ..utils.apiConnection import apiConnection
from ..utils.checker import getURL
from ..objects.Asset import Asset
from ..objects.AssetManagementData import AssetManagementData
from ..objects.AssetManagementResult import AssetManagementResult
from ..objects.QuantumExecutionHistoryEntry import QuantumExecutionHistoryEntry
from ..circuit.annealing.CircuitAnnealing import CircuitAnnealing
from ..circuit.gates.CircuitGates import CircuitGates
from ..circuit.flow.CircuitFlow import CircuitFlow

from datetime import datetime
import time
import base64


# API ENDPOINTS
dynamicExtensions = {
    'getAssetCatalog': 'connectionPoint/getAssetCatalog/',
    'getAsset': 'connectionPoint/getAsset/',
    'createAsset': 'connectionPoint/createAsset?aSolutionID=',
    'updateAsset': 'connectionPoint/updateAsset/',
    'getAssetManagementResult': 'connectionPoint/getAssetManagementResult/',
    'publishFlow': 'connectionPoint/publishFlow/',
    'deleteAsset': 'connectionPoint/deleteAsset/',
    'getQuantumExecutionHistoric': 'connectionPoint/getQuantumExecutionHistoric/',
    'getQuantumExecutionHistoricResult': 'connectionPoint/getQuantumExecutionHistoricResult/'
}


##################_____DYNAMIC METHODS_____##################

# GET ASSET CATALOG
def getAssetCatalog(self, context, idSolution: int, assetType: str, assetLevel: str) -> list:
    urlData = getURL(context)
    url = urlData[0] + dynamicExtensions['getAssetCatalog'] + str(idSolution) + '/' + assetType + '/' + assetLevel
    validate = urlData[1]

    assetCatalog = []

    assetCatalogList = apiConnection(url, context.getHeader(), 'json', validate=validate)

    for asset in assetCatalogList:
        assetCatalog.append(Asset(asset))

    return assetCatalog

# GET ASSET
def getAsset(self, context, idAsset: int, assetType: str, assetLevel: str) -> Asset:
    urlData = getURL(context)
    url = urlData[0] + dynamicExtensions['getAsset'] + str(idAsset) + '/' + assetType + '/' + assetLevel
    validate = urlData[1]

    assetResponse = apiConnection(url, context.getHeader(), 'json', validate=validate)
    
    return Asset(assetResponse)

# CREATE ASSET
def createAsset(self, context, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody, assetType: str,
                assetLevel: str) -> AssetManagementData:
    if isinstance(assetBody, (CircuitGates, CircuitAnnealing, CircuitFlow)):
        assetBody = assetBody.getParsedBody()

    newAsset = {
        "AssetID": -1,
        "AssetName": assetName,
        "AssetNamespace": assetNamespace,
        "AssetDescription": assetDescription,
        "AssetBody": base64.b64encode(assetBody.encode('ascii')).decode('ascii'),
        "AssetType": assetType,
        "AssetLevel": assetLevel,
        "AssetLastUpdate": ''
    }

    urlData = getURL(context)
    url = urlData[0] + dynamicExtensions['createAsset'] + str(idSolution)
    validate = urlData[1]
    
    assetManagementDataResult = apiConnection(url, context.getHeader(), str(newAsset), 'json', 'data', validate=validate)

    return AssetManagementData(assetManagementDataResult)

# CREATE ASSET SYNC
def createAssetSync(self, context, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody, assetType: str,
                    assetLevel: str) -> AssetManagementResult:

    assetManagementData = createAsset(None, context, idSolution, assetName, assetNamespace, assetDescription, assetBody, assetType, assetLevel)
    assetManagementResult = getAssetManagementResult(None, context, assetManagementData.getLifecycleToken())

    while assetManagementResult.getExitCode() == 'WAIT' or assetManagementResult.getExitCode() == 'READY':
        time.sleep(1)
        assetManagementResult = getAssetManagementResult(None, context, assetManagementData.getLifecycleToken())

    return assetManagementResult

# CREATE ASSET FLOW
def createAssetFlow(self, context, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody, assetLevel: str,
                    publish: bool = False) -> AssetManagementData:

    assetManagementData = createAsset(None, context, idSolution, assetName, assetNamespace, assetDescription, assetBody, 'FLOW', assetLevel)

    if publish: publishFlow(None, context, assetManagementData.getIdAsset(), publish)

    return assetManagementData

# CREATE ASSET FLOW SYNC
def createAssetFlowSync(self, context, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody, assetLevel: str,
                        publish: bool = False) -> AssetManagementResult:
    
    assetManagementData =createAssetFlow(None, context, idSolution, assetName, assetNamespace, assetDescription, assetBody, assetLevel, publish)
    assetManagementResult = getAssetManagementResult(None, context, assetManagementData.getLifecycleToken())

    while assetManagementResult.getExitCode() == 'WAIT' or assetManagementResult.getExitCode() == 'READY':
        time.sleep(1)
        assetManagementResult = getAssetManagementResult(None, context, assetManagementData.getLifecycleToken())

    return assetManagementResult

# PUBLISH FLOW
def publishFlow(self, context, idFlow: int, publish: bool) -> bool:
    urlData = getURL(context)
    url = urlData[0] + dynamicExtensions['publishFlow'] + str(idFlow) + '/' + str(publish)
    validate = urlData[1]

    apiConnection(url, context.getHeader(), 'string', validate=validate)
    
    return publish

# UPDATE ASSET
def updateAsset(self, context, asset: Asset, assetName: str = None, assetNamespace: str = None, assetDescription: str = None, assetBody = None,
                assetType: str = None, assetLevel: str = None) -> AssetManagementData:
    
    if assetName:
        asset.setName(assetName)
    if assetNamespace:
        asset.setNamespace(assetNamespace)
    if assetDescription:
        asset.setDescription(assetDescription)
    if assetBody:
        if isinstance(assetBody, (CircuitGates, CircuitAnnealing, CircuitFlow)):
            assetBody = assetBody.getParsedBody()
        asset.setBody(assetBody)
    if assetType:
        asset.setType(assetType)
    if assetLevel:
        asset.setLevel(assetLevel)

    newAsset = {
        "AssetID": asset.getId(),
        "AssetName": asset.getName(),
        "AssetNamespace": asset.getNamespace(),
        "AssetDescription": asset.getDescription() if asset.getDescription() else '',
        "AssetBody": base64.b64encode(asset.getBody().encode('ascii')).decode('ascii'),
        "AssetType": asset.getType(),
        "AssetLevel": asset.getLevel(),
        "AssetLastUpdate": asset.getLastUpdate()
    }
    
    urlData = getURL(context)
    url = urlData[0] + dynamicExtensions['updateAsset']
    validate = urlData[1]

    assetManagementDataResult = apiConnection(url, context.getHeader(), str(newAsset), 'json', 'data', validate=validate)
    
    return AssetManagementData(assetManagementDataResult)

# UPDATE ASSET SYNC
def updateAssetSync(self, context, asset: Asset, assetName: str = None, assetNamespace: str = None, assetDescription: str = None, assetBody = None,
                    assetType: str = None, assetLevel: str = None) -> AssetManagementResult:

    assetManagementData = updateAsset(None, context, asset, assetName, assetNamespace, assetDescription, assetBody, assetType, assetLevel)
    assetManagementResult = getAssetManagementResult(None, context, assetManagementData.getLifecycleToken())

    while assetManagementResult.getExitCode() == 'WAIT' or assetManagementResult.getExitCode() == 'READY':
        time.sleep(1)
        assetManagementResult = getAssetManagementResult(None, context, assetManagementData.getLifecycleToken())

    return assetManagementResult

# GET ASSET MANAGEMENT RESULT
def getAssetManagementResult(self, context, lifecycleToken: str) -> AssetManagementResult:
    urlData = getURL(context)
    url = urlData[0] + dynamicExtensions['getAssetManagementResult'] + str(lifecycleToken)
    validate = urlData[1]

    assetManagementResult = apiConnection(url, context.getHeader(), 'json', validate=validate)

    return AssetManagementResult(assetManagementResult)

# DELETE ASSET
def deleteAsset(self, context, *args) -> bool:
    if len(args) == 1:
        idAsset = str(args[0].getId())

        if args[0].getType() == 'FLOW':
            assetType = args[0].getType()
        else:
            assetType = 'CIRCUIT'

    else:
        idAsset = str(args[0])
        assetType = str(args[1])

    urlData = getURL(context)
    url = urlData[0] + dynamicExtensions['deleteAsset'] + idAsset + '/' + assetType
    validate = urlData[1]

    return apiConnection(url, context.getHeader(), 'boolean', validate=validate)

# GET QUANTUM EXECUTION HISTORIC
def getQuantumExecutionHistoric(self, context, idSolution: int = None, idFlow: int = None, idDevice: int = None, dateFrom: str = None, isSimulator: bool = None,
                                top: int = None, resultType: bool = None) -> list:

    quantumExecutionHistoric = list()

    if dateFrom:
        t0 = datetime(1, 1, 1)
        now = datetime.strptime(dateFrom, '%Y-%m-%dT%H:%M:%S')
        seconds = (now - t0).total_seconds()
        dateFrom = int(seconds * 10**7)

    urlData = getURL(context)
    url = urlData[0] + dynamicExtensions['getQuantumExecutionHistoric'] + str(idSolution) + '/' + str(idFlow) + '/' + str(idDevice) + '/' + str(dateFrom) + '/' + str(isSimulator) + '/' + str(top) + '/' + str(resultType)
    validate = urlData[1]

    quantumExecutionHistoricList = apiConnection(url, context.getHeader(), 'json', validate=validate)

    for quantumExecutionHistoryEntry in quantumExecutionHistoricList:
        quantumExecutionHistoric.append(QuantumExecutionHistoryEntry(quantumExecutionHistoryEntry))

    return quantumExecutionHistoric

def getQuantumExecutionHistoricResult(self, context, idResult: int) -> QuantumExecutionHistoryEntry: # getQuantumExecutionHistoricResult. Returns a QuantumExecutionHistoryEntry object
    urlData = getURL(context)
    url = urlData[0] + dynamicExtensions['getQuantumExecutionHistoricResult'] + str(idResult)
    validate = urlData[1]

    quantumExecutionHistoricResultList = apiConnection(url, context.getHeader(), 'json', validate=validate)
            
    return QuantumExecutionHistoryEntry(quantumExecutionHistoricResultList[0])