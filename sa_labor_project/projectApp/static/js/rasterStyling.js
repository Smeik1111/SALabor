import { colorGrades, gradeStart, gradeSteps } from "./constants.js";
// Styling für einen Datenpunkt / eine Rasterfläche
export function style(feature) {
    return {
        fillColor: getColor(feature.properties.CO),
        weight: 2,
        opacity: 1,
        color: '',
        dashArray: '0',
        fillOpacity: 0.7
    };
}

// Annhame: Die CO-Werte liegen für gewöhnlich zwischen 0 und 100+
function getColor(coValue) {
    const maxGrade = colorGrades.length;
    const adjustedCoValue = Math.max(0, coValue - gradeStart);
    const grade = Math.min(Math.ceil(adjustedCoValue / gradeSteps), maxGrade);
    return colorGrades[grade];
}