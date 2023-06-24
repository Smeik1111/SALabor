const baseUrl = 'http://localhost:8000';
export const countriesUrl = baseUrl + '/projectApp/countries';

export const colorGrades = ['#ffffd9', '#edf8b1', '#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0', '#225ea8', '#253494', '#081d58'];
export const gradeSteps = 5;
export const gradeStart = 60
export const grades = colorGrades.map((color, idx) => idx === 0 ? 0 : (idx - 1) * gradeSteps + gradeStart);