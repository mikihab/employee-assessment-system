const envoirnment = process.env.NODE_ENV;
/*const apis={
    BASE_LOCAL_URL:'http://localhost:3000',
    BASE : "http://localhost:5000",
    LOGIN : "/api/v1/login/",
    GETDETAILSUSER : "/api/v1/user/details",
    GET_ALL_TRAINER :'/api/v1/admin/trainer/details/all',
    GET_SINGLE_TRAINER_DETAILS : '/api/v1/admin/trainer/details',
    CREATE_TRAINER : '/api/v1/admin/trainer/create',
    DELETE_TRAINER : '/api/v1/admin/trainer/remove',
    GET_ALL_SUBJECTS : '/api/v1/subject/details/all',
    GET_SINGLE_SUBJECT_DETAILS : '/api/v1/subject/details',
    CREATE_SUBJECT : '/api/v1/subject/create',
    GET_ALL_QUESTIONS : '/api/v1/questions/details/all',
    DELETE_QUESTION:'/api/v1/questions/delete',
    FETCH_SINGLE_QUESTION:'/api/v1/questions/details',
    CREATE_QUESTIONS :'/api/v1/questions/create',
    FILE_UPLOAD:'/api/v1/upload',
    CREATE_TEST : '/api/v1/test/create',
    GET_ALL_TESTS:'/api/v1/test/details/all',
    GET_SINGLE_TEST:'/api/v1/test/trainer/details',
    REGISTER_TRAINEE_FOR_TEST:'/api/v1/trainee/enter',
    RESEND_TRAINER_REGISTRATION_LINK: '/api/v1/trainee/resend/testlink',
    GET_SINGLE_TEST_DETAILS_BASIC:'/api/v1/test/basic/details',
    STOP_REGISTRATION :'/api/v1/trainer/registration/stop',
    START_TEST_BY_TRAINER:'/api/v1/test/begin',
    GET_TEST_CANDIDATES :'/api/v1/test/candidates',
    GET_TEST_QUESTIONS :'/api/v1/test/questions',
    FETCH_TRAINEE_DETAILS:'/api/v1/trainee/details',
    FETCH_TRAINEE_TEST_DETAILS:'/api/v1/trainee/flags',
    PROCEED_TO_TEST:'/api/v1/trainee/answersheet',
    FETCH_TRAINEE_TEST_QUESTION:'/api/v1/trainee/paper/questions',
    FETCH_TRAINEE_TEST_ANSWERSHEET:'/api/v1/trainee/chosen/options',
    UPDATE_ANSWERS:'/api/v1/trainee/update/answer',
    END_TEST : '/api/v1/trainee/end/test',
    FETCH_OWN_RESULT:'/api/v1/final/results',
    FETCH_SINGLE_QUESTION_BY_TRAINEE:'/api/v1/trainee/get/question',
    END_TEST_BY_TRAINER:'/api/v1/test/end',
    FEEDBACK_STATUS_CHECK:'/api/v1/trainee/feedback/status',
    GIVE_FEEDBACK:'/api/v1/trainee/feedback',
    GET_STATS:'/api/v1/test/candidates/details',
    GET_EXCEL:'/api/v1/trainer/result/download',
    MAX_MARKS_FETCH:'/api/v1/test/max/marks'
}*/
const apis = {
  BASE_LOCAL_URL: envoirnment === "development" ? "http://localhost:3000" : "",
  BASE: envoirnment === "development" ? "http://localhost:8000" : "",
  LOGIN: "/login",
  GETUSER: "/user",
  GET_ALL_TRAINER: "/user",
  GET_SINGLE_TRAINER_DETAILS: "/user/",
  CREATE_TRAINER: "/user",
  DELETE_TRAINER: "/user/",
  GET_ALL_SUBJECTS: "/api/v1/subject/details/all",
  GET_SINGLE_SUBJECT_DETAILS: "/api/v1/subject/details",
  CREATE_SUBJECT: "/api/v1/subject/create",
  GET_ALL_QUESTIONS: "/api/v1/questions/details/all",
  DELETE_QUESTION: "/api/v1/questions/delete",
  FETCH_SINGLE_QUESTION: "/api/v1/questions/details",
  CREATE_QUESTIONS: "/api/v1/questions/create",
  FILE_UPLOAD: "/api/v1/upload",
  CREATE_TEST: "/exam",
  GET_ALL_TESTS: "/api/v1/test/details/all",
  GET_SINGLE_TEST: "/api/v1/test/trainer/details",
  REGISTER_TRAINEE_FOR_TEST: "/api/v1/trainee/enter",
  RESEND_TRAINER_REGISTRATION_LINK: "/api/v1/trainee/resend/testlink",
  GET_SINGLE_TEST_DETAILS_BASIC: "/api/v1/test/basic/details",
  STOP_REGISTRATION: "/api/v1/trainer/registration/stop",
  START_TEST_BY_TRAINER: "/api/v1/test/begin",
  GET_TEST_CANDIDATES: "/api/v1/test/candidates",
  GET_TEST_QUESTIONS: "/api/v1/test/questions",
  FETCH_TRAINEE_DETAILS: "/api/v1/trainee/details",
  FETCH_TRAINEE_TEST_DETAILS: "/api/v1/trainee/flags",
  PROCEED_TO_TEST: "/api/v1/trainee/answersheet",
  FETCH_TRAINEE_TEST_QUESTION: "/api/v1/trainee/paper/questions",
  FETCH_TRAINEE_TEST_ANSWERSHEET: "/api/v1/trainee/chosen/options",
  UPDATE_ANSWERS: "/api/v1/trainee/update/answer",
  END_TEST: "/api/v1/trainee/end/test",
  FETCH_OWN_RESULT: "/api/v1/final/results",
  FETCH_SINGLE_QUESTION_BY_TRAINEE: "/api/v1/trainee/get/question",
  END_TEST_BY_TRAINER: "/api/v1/test/end",
  FEEDBACK_STATUS_CHECK: "/api/v1/trainee/feedback/status",
  GIVE_FEEDBACK: "/api/v1/trainee/feedback",
  GET_STATS: "/api/v1/test/candidates/details",
  GET_EXCEL: "/api/v1/trainer/result/download",
  MAX_MARKS_FETCH: "/api/v1/test/max/marks",
  GET_FEEDBACKS: "/api/v1/trainer/get/feedbacks",
  CHECK_TEST_NAME: "/api/v1/test/new/name/check",
};

export default apis;
