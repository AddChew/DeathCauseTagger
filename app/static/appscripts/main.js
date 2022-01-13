const dateFormat = d3.timeFormat('%c')
const icdCodesMatchingScriptPath = '/static/appscripts/icdCodesMatching.js'

let removeElementById = id => {
    const element = document.getElementById(id)
    if (document.contains(element)) element.remove()
}

let removeChildNodes = parent => {
    while (parent.firstChild) parent.removeChild(parent.firstChild)
}

let createElement = (tag, text=null, value=null, id=null, href=null, download=null) => {
    const element = document.createElement(tag)
    if (text) element.appendChild(document.createTextNode(text))
    if (value) element.setAttribute('value', value)
    if (id || id === 0) element.setAttribute('id', id)
    if (href) element.setAttribute('href', href)
    if (download) element.setAttribute('download', download)
    return element
}

let setPageLayout = layout => {
    switch(layout){
        case 'center':
            document.querySelector('div').style.justifyContent = 'center'
            break
        case 'flex-start':
            document.querySelector('div').style.justifyContent = 'flex-start'
            break
    }
}

let setPlaceholder = (placeholder, disabled=true) => [{value: '', label: placeholder, selected:true, disabled: disabled}]

let renderTemplate = (templateid, parentid=null, parentTag=null) => {
    const template = document.getElementById(templateid)
    const content = template.content.cloneNode(true) 
    if (parentid){
        document.getElementById(parentid).append(content)
        return
    }
    if (parentTag) document.querySelector(parentTag).append(content)  
}

let renderColumnSelector = (id, template_id, parent_id) => {
    if (!document.getElementById(id)) renderTemplate(template_id, parentid = parent_id)
}

let renderDataTableContainer = templateid => {
    setPageLayout('flex-start')
    removeElementById('sub-container-2')
    renderTemplate(templateid, parentid = null, parentTag = 'div')
}

let renderSubmitButton = () =>{
    removeElementById('submitButton')
    if (causeDescColOptions.getValue(true) && illnessPeriodColOptions.getValue(true)) renderTemplate('submitButtonTemplate', parentid = 'fileSelector')
}

let renderDownloadButton = () =>{
    removeElementById('downloadButton')
    renderTemplate('downloadButtonTemplate', parentid = 'sub-container-1')
}

let renderLabellingPage = () => {
    removeElementById('progress')
    document.querySelector('legend').textContent = 'Please select only one ICD code from Suggested ICD Codes or Full List of ICD Codes'
    renderTemplate('dataLabelingContentTemplate', parentid = 'dataLabelingContainer')
    loadNextPage()
    updateLabellingProgress(fuzzyMatches, {})
}

let populateCauseDescDropdown = columns => {
    if (typeof causeDescColOptions === 'undefined'){
        const dropdownElement = document.querySelector('#causeDescColSelector select')
        causeDescColOptions = new Choices(dropdownElement, {shouldSort: false}) 
    }
    causeDescColOptions.clearChoices()
    causeDescColOptions.setChoices(
        setPlaceholder('Please Select Cause Description Column').concat(
        columns.map((column) => {
            return {value: column, label: column}
        })))
    renderSubmitButton()
}

let populateIllnessPeriodDropdown = columns => {
    if (typeof illnessPeriodColOptions === 'undefined'){
        const dropdownElement = document.querySelector('#timePeriodColSelector select')
        illnessPeriodColOptions = new Choices(dropdownElement, {shouldSort: false}) 
    }
    illnessPeriodColOptions.clearChoices()
    illnessPeriodColOptions.setChoices(
        setPlaceholder('Please Select Illness Period Column').concat(
        columns.map((column) => {
            return {value: column, label: column}
        })))
    renderSubmitButton()
}

let populateicdDropdownList = () => {
    if (typeof icdDropdown === 'undefined') {
        const icdDropdownElement = document.getElementById('allOptions')
        icdDropdown = new Choices(icdDropdownElement, {shouldSort: false})
        icdDropdown.setChoices(
            [{label: '', choices: setPlaceholder('No ICD Code Selected', false)}].concat(icdDropdownList)
            )
    }
    icdDropdown.setChoiceByValue('') 
}

let populateSuggestedDropdownList = () => {
    if (typeof suggestedICDcodes === 'undefined') {
        const suggestedDropdownElement = document.getElementById('suggestedOptions')
        suggestedICDcodes = new Choices(suggestedDropdownElement, {shouldSort: false})
    }
    suggestedICDcodes.setChoices(
        setPlaceholder('No ICD Code Selected', false).concat(fuzzyMatches[currentIndex].ICD_CD_PRED),
        'value',
        'label',
        replaceChoices=true
    )
}

let populateHeader = headerArray => {
    headerArray.forEach((header) => {
        const headerCol = createElement('th', text=header)
        document.querySelector('tr').appendChild(headerCol)
    })
}

let populateDataRow = (row, id=null) => {
    const rowValues = Object.values(row)
    const elementIdExists = document.getElementById(id)
    const rowContainer = elementIdExists || (id || id === 0 ? createElement('tr', null, null, id) : createElement('tr'))
    removeChildNodes(rowContainer)
    rowValues.forEach((rowValue) => {
        const column = createElement('td', text=rowValue)
        rowContainer.appendChild(column)
    })
    if (!elementIdExists) document.querySelector('tbody').appendChild(rowContainer)
}

let populateDataRows = rows => rows.forEach((row) => populateDataRow(row))

let populateTable = parsedContent => {
    populateHeader(parsedContent.columns)
    populateDataRows(parsedContent)
}

let readFile = file => {
    return new Promise((resolve, reject) => {
        const fileReader = new FileReader()
        fileReader.onload = () => resolve(fileReader.result)
        fileReader.onerror = () => reject
        fileReader.readAsDataURL(file)
    })
}

let parseFile = async () => {
    const file = document.querySelector('input').files[0]
    const fileContent = await readFile(file)
    const parsedContent = d3.csv(fileContent)
    return parsedContent
}

let getFileInfo = () => {
    const file = document.querySelector('input').files[0]
    return`<strong>${file.name}</strong>
            (${file.type}) - ${file.size} bytes, 
            last modified: ${dateFormat(file.lastModifiedDate)}`
}

let displayFileInfo = async () => {
    const fileInfo = getFileInfo()
    document.querySelector('ul').style.display = 'block'
    document.querySelector('li').innerHTML = fileInfo
    renderDataTableContainer('dataTableTemplate')
    parsedContent = await parseFile()
    removeElementById('progress')
    populateTable(parsedContent)

    renderColumnSelector('causeDescColSelector', 'causeDescColSelectorTemplate', 'fileSelector')
    populateCauseDescDropdown(parsedContent.columns)

    renderColumnSelector('timePeriodColSelector', 'timePeriodColSelectorTemplate', 'fileSelector')
    populateIllnessPeriodDropdown(parsedContent.columns)
}

let loadingPage = async() => {
    causeDescColumn = document.querySelector('#causeDescColSelector select').value
    illnessPeriodColumn = document.querySelector('#timePeriodColSelector select').value
    removeElementById('fileSelector')
    removeElementById('sub-container-2')
    setPageLayout('center')
    renderTemplate('dataLabelingContainerTemplate', parentid = 'sub-container-1');
    [exactMatches, fuzzyMatches, icdDropdownList] = await sendMatchingJobToWebWorker(
        icdCodesMatchingScriptPath, 
        postMessage=[causeDescColumn, illnessPeriodColumn, parsedContent])
    fuzzyMatches.length === 0 ? renderDownloadButton() : renderLabellingPage()
}

let sendMatchingJobToWebWorker = (scriptPath, postMessage) => {
    if (typeof(Worker)){
        return new Promise ((resolve) => {
            const worker = new Worker(scriptPath)
            worker.postMessage(postMessage)
            worker.onmessage = msg => {
                const increment = 100/parsedContent.length||0
                if (msg.data) resolve(msg.data)
                updateProgressBar(increment)
            }
        })
    } 
}

let updateProgressBar = increment => {
    document.querySelector('progress').value += increment
    const percentCompleted = Math.floor(document.querySelector('progress').value)
    document.getElementById('percentCompleted').textContent = `${percentCompleted}%`   
}

let loadNextPage = (increment = 1) => {
    if (typeof currentIndex === 'undefined') currentIndex = -1
    currentIndex += increment
    currentIndex = Math.min(currentIndex, fuzzyMatches.length-1);
    document.querySelector('output.causeDesc').value = fuzzyMatches[currentIndex][causeDescColumn]
    document.querySelector('output.illnessPeriod').value = `${fuzzyMatches[currentIndex][illnessPeriodColumn]} DAY(S)`
    populateicdDropdownList()
    populateSuggestedDropdownList() 
    toggleButtonStates() 
}

let toggleButtonStates = () => {
    if (fuzzyMatches.length === 1){
        document.getElementById('prev').disabled = true
        document.getElementById('next').disabled = true
        renderDownloadButton()
        return
    }
    switch(currentIndex){
        case 0:
            document.getElementById('prev').disabled = true
            break
        case fuzzyMatches.length - 1:
            document.getElementById('next').disabled = true
            renderDownloadButton()
            break
        default: 
            removeElementById('downloadButton')
            document.getElementById('prev').disabled = false
            document.getElementById('next').disabled = false
    }
}

let submit = () => {
    const selectedICDcode = checkSelectedOptions()
    if (selectedICDcode){
        appendToLabelled(selectedICDcode)
        if (!document.getElementById('sub-container-2')){
            renderDataTableContainer('labelledTableTemplate')
            populateHeader(Object.keys(labelledMatches[currentIndex]))
        }
        populateDataRow(labelledMatches[currentIndex], currentIndex)
        loadNextPage()
        updateLabellingProgress(fuzzyMatches, labelledMatches)
    }
}

let appendToLabelled = selectedICDcode => {
    const [icdCode, icdDesc] = selectedICDcode.split(' - ')
    let currentRow = {...fuzzyMatches[currentIndex]}
    currentRow.ICD_CD_PRED = icdCode
    currentRow.ICD_CD_DESC = icdDesc
    if (typeof labelledMatches === 'undefined') labelledMatches = {}
    labelledMatches[currentIndex] = currentRow
}

let checkSelectedOptions = () => {
    if (suggestedICDcodes.getValue(true) && icdDropdown.getValue(true)){
        alert('Please select only one ICD code from Suggested ICD Codes or Full List of ICD Codes!')
        return 
    }
    if (!suggestedICDcodes.getValue(true) && !icdDropdown.getValue(true)){
        alert('Please select an ICD code from Suggested ICD Codes or Full List of ICD Codes!')
        return
    }
    return suggestedICDcodes.getValue(true)||icdDropdown.getValue(true)
}

let updateLabellingProgress = (totalToBeLabelled, labelled) => {
    const numLabelled = Object.keys(labelled).length
    const remainder = totalToBeLabelled.length - numLabelled
    document.querySelector('p').textContent = `${numLabelled} record(s) labelled, ${remainder} record(s) remaining.`
}

let downloadICDcodes = () => {
    const labelledMatchesArray = typeof labelledMatches === 'undefined' ? [] : Object.values(labelledMatches)
    const allMatches = [...exactMatches, ...labelledMatchesArray]
    convertToDownloadLink(allMatches, 'allMatches', 'Matched ICD Codes.csv')
    if (labelledMatchesArray.length){
        const newlabelsMap = labelledMatchesArray.map((row) => {
            const {[causeDescColumn]: CAUSE_DESC, ICD_CD_PRED} = row
            return {CAUSE_DESC, ICD_CD_PRED}
        })
        convertToDownloadLink(newlabelsMap, 'newLabelsMap', 'New Labels Map.csv')
    }
}

let convertToDownloadLink = (dataArray, id, downloadFileName) => {
    const csv = d3.csvFormat(dataArray)
    const csvBlob = new Blob([csv], {type: 'text/csv;'})
    const csvURL = URL.createObjectURL(csvBlob)
    const downloadLink = createElement('a', null, null, id, csvURL, downloadFileName)
    document.querySelector('div').append(downloadLink)
    document.getElementById(id).click()
    removeElementById(id)
}