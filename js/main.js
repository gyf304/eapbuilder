appConfig = {
  courseListJsonUrl: 'data/courselist.json'
}

Vue.component('modal', {
  template: '#modal-template'
})

appData = {
  state: 'intro',
  showModal: false,
  stateIndex: 0,
  states: ['intro', 'audit', 'review', 'print'],
  ready: false,
  message: 'Hello Vue!',
  auditInput: '',
  audits: [],
  auditConstants: {
    semesters: ['Fall', 'Spring', 'Sum1', 'Sum2'],
    grades: [ '*' , 'P', 'F' , 
              'A+', 'A', 'A-', 
              'B+', 'B', 'B-', 
              'C+', 'C', 'C-', 
              'D+', 'D', 'D-', 
              'R' , 'W', 'TR']
  },
  auditModifyInfo: {
    modifyIndex: null,
    fields: {
      'course_number': {
        'value': '',
        'validator': function(val){return /^[0-9X]{2}\-[0-9X]{3}$/.test(val)},
        'hint': 'Course number should be in the form of XX-XXX (eg. 15-122)'
      },
      'course_name': {
        'value': '',
        'validator': function(val){return true},
        'hint': 'Course Name'
      },
      'grade': {
        'value': '',
        'validator': function(val){
          for (var i = 0; i < appData.auditConstants.grades.length; i++) {
            var e = appData.auditConstants.grades[i];
            if (val == e) return true
          }
          return false
        },
        'hint': 'Select grade from drop-down'
      },
      'units': {
        'value': '',
        'validator': function(val){return /^[0-9]{1,2}[\.]*[0-9]*$/.test(val)},
        'converter': parseFloat,
        'hint': 'Units should be in the form of XX.X, like "12.0". Entering "12" is also acceptable.'
      },
      'instance': {
        'value': {'semester':'', 'year':''},
        'validator': function(val){
          for (var i = 0; i < appData.auditConstants.semesters.length; i++) {
            var e = appData.auditConstants.semesters[i];
            if (val.semester == e && /^[0-9]{2}$/.test(val.year)) return true
          }
          return false
        },
        'converter': function(val) {return {'semester': val.semester, 'year': parseInt(val.year)}},
        'hint': 'Select semester from drop-down. Year should be 2 digits (eg. 17 for year 2017)'
      }
    }
  },
  courses: {},
  printData: {
    items: []
  },
  eapModifyInfo: {
    'show': false
  }
}

var app = new Vue({
  el: '#app',
  data: appData,
  methods: {
    'snackbar': function(msg) {
      var x = document.getElementById("snackbar")
      x.className = "show"
      x.innerText = msg
      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000)
    },
    'processAuditInput': function(input) {
      var result = invokePython('parseAudit', [input], {})
      appData.audits.push(result)
    },
    'showModifyCourseModal': function(auditIndex,categoryIndex,courseIndex){
      appData.auditModifyInfo.modifyIndex = [auditIndex, categoryIndex, courseIndex]
      var data = appData.audits[auditIndex][categoryIndex].courses[courseIndex]
      var fields = appData.auditModifyInfo.fields
      for (var key in fields) {
        if (fields.hasOwnProperty(key)) {
          fields[key].value = data[key]
        }
      }
      appData.eapModifyInfo.show = true;
    },
    'hideModifyCourseModal': function(auditIndex,categoryIndex,courseIndex){
      appData.eapModifyInfo.show = false;
    },
    'deleteCourse': function(auditIndex, categoryIndex, courseIndex) {
      category = appData.audits[auditIndex][categoryIndex]
      category.courses.splice(courseIndex,1)
    },
    'addDummyCourse': function(auditIndex, categoryIndex) {
      var data = {
        'course_number': 'XX-XXX',
        'course_name': 'To be filled',
        'instance': {
          'semester': 'Fall',
          'year': 00
        },
        'grade': '*',
        'units': 0.0
      }
      appData.audits[auditIndex][categoryIndex].courses.push(data)
    },
    'modifyCourseFromModal': function(){
      var errors = this.getCourseModifyModalErrors()
      if (errors.length > 0) return false
      var fields = appData.auditModifyInfo.fields
      var data = {}
      for (var key in fields) {
        if (fields.hasOwnProperty(key)) {
          var converter = fields[key].converter
          if (converter) {
            data[key] = converter(fields[key].value)
          } else {
            data[key] = fields[key].value
          }
        }
      }
      var auditIndex = appData.auditModifyInfo.modifyIndex[0]
      var categoryIndex = appData.auditModifyInfo.modifyIndex[1]
      var courseIndex = appData.auditModifyInfo.modifyIndex[2]
      this.$set(appData.audits[auditIndex][categoryIndex].courses, courseIndex, data)
      return true
    },
    'getCourseModifyModalErrors': function() {
      var fields = appData.auditModifyInfo.fields
      var errors = []
      for (var key in fields) {
        if (fields.hasOwnProperty(key)) {
          var value = fields[key].value
          var validator = fields[key].validator
          var isValid = validator(value)
          if (!isValid){
            errors.push(fields[key].hint)
          }
        }
      }
      return errors
    },
    'zip': function(arr1, arr2){
      var maxlen = arr1.length > arr2.length ? arr1.length : arr2.length
      var result = []
      for (var i = 0; i<maxlen; i++) {
        result.push([arr1[i], arr2[i]])
      }
      return result
    },
    'deleteEapItem': function(itemIndex) {
      appData.printData.items.splice(itemIndex, 1)
    },
    'swapEapItems': function(itemIndex1, itemIndex2) {
      var len = appData.printData.items.length
      if (itemIndex1 < 0 || itemIndex1 >= len) return
      if (itemIndex2 < 0 || itemIndex2 >= len) return
      var tmp = appData.printData.items[itemIndex1]
      this.$set(appData.printData.items, itemIndex1, appData.printData.items[itemIndex2])
      this.$set(appData.printData.items, itemIndex2, tmp)
    },
    'generate': function() {
      var ret = invokePython('genEap', [appData.audits], [])
      this.$set(appData.printData, 'items', ret)
    },
    'print': function() {
      window.print()
    }
  }
})

console.log("hello")

function init(){
  brython({debug:1, pythonpath:['py']})
  jQuery.getJSON(appConfig.courseListJsonUrl, null, function(data){
    appData.courses = data
    appData.ready = true
  })
}

function invokePython(func, args, kwargs) {
  return JSON.parse(rawInvokePython(func, JSON.stringify([args, kwargs])))
}