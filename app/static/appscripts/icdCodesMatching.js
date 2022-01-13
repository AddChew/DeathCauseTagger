importScripts('./jslibs/fuzzball.umd.min.js')
const icdDictJson = './json/icd_codes.json'
const dropdownJson = './json/icdCodesFullDropdown.json'
const timePeriodJson = './json/time_period.json'

let loadJson = async (icdDictJson, dropdownJson, timePeriodJson) => {
    const icdResponse = await fetch(icdDictJson)
    const {icd_cause, cause_icd} = await icdResponse.json()
    icdCause = icd_cause
    causeIcd = cause_icd
    allCauses = Object.keys(causeIcd)

    const dropdownResponse = await fetch(dropdownJson) 
    icdDropdownList = await dropdownResponse.json()

    const timePeriodResponse = await fetch(timePeriodJson)
    timePeriod = await timePeriodResponse.json()
}

let removeNonAlpha = string => string.replace(/[^0-9A-Z ]/g, ' ').replace(/\s+/g, ' ').trim()

let exactMatch = (row, cleanCauseDesc, illnessPeriod) => {
    let icdCode = causeIcd[cleanCauseDesc]
    icdCode = timePeriod.hasOwnProperty(icdCode) ? timePeriodMatch(icdCode, illnessPeriod) : icdCode
    row.ICD_CD_PRED = icdCode
    row.ICD_CD_DESC = icdCause[icdCode]
    exactMatches.push(row)
}

let timePeriodMatch = (icdCode, illnessPeriod) => {
    if (illnessPeriod === '') return icdCode
    const {THRESHOLD, ICD_CD_LESS, ICD_CD_EQUAL, ICD_CD_MORE} = timePeriod[icdCode]
    if (illnessPeriod < THRESHOLD) return ICD_CD_LESS
    else if (illnessPeriod === THRESHOLD) return ICD_CD_EQUAL
    else return ICD_CD_MORE
}

let fuzzyMatch = (row, cleanCauseDesc, illnessPeriod) => {
    const top3causes = fuzzball.extract(cleanCauseDesc, allCauses, fuzzball.token_set_ratio).slice(0, 3).map(result => result[0]) 
    const top3icdCodeDesc = top3causes.map(cause => {
        let icdCode = causeIcd[cause]
        icdCode = timePeriod.hasOwnProperty(icdCode) ? timePeriodMatch(icdCode, illnessPeriod) : icdCode
        const option = `${icdCode} - ${icdCause[icdCode]}`
        return {value: option, label: option}
    })
    row.ICD_CD_PRED = top3icdCodeDesc
    fuzzyMatches.push(row)
}

let getICDCode = (row, causeDescColumn, illnessPeriodColumn) => {
    const cleanCauseDesc = removeNonAlpha(row[causeDescColumn])
    const illnessPeriod = row[illnessPeriodColumn]
    causeIcd.hasOwnProperty(cleanCauseDesc) ? exactMatch(row, cleanCauseDesc, illnessPeriod) : fuzzyMatch(row, cleanCauseDesc, illnessPeriod)
}

let getICDCodes = () => {
    exactMatches = []
    fuzzyMatches = []
    parsedContent.forEach(row => {
        getICDCode(row, causeDescColumn, illnessPeriodColumn)
        postMessage(null)
    })  
}

onmessage = async (msg) => {
    [causeDescColumn, illnessPeriodColumn, parsedContent] = msg.data
    await loadJson(icdDictJson, dropdownJson, timePeriodJson)
    getICDCodes()
    postMessage([exactMatches, fuzzyMatches, icdDropdownList]) 
}