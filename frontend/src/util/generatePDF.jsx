import jsPDF from 'jspdf';

//task 26 generate pdf report from fit score, matched keywords, and feedback
export function generatePDF(fitScore, matchedKeywords, feedback) {
    const doc = new jsPDF();
    
    //add current date to top of pdf for more relevancy
    const currentDate = new Date().toLocaleDateString();
    doc.setFontSize(18);
    doc.setFont("times", "bold");
    doc.text("Resume Analysis Report", 105, 10, { align: 'center', underline: true });
    doc.setFontSize(12);
    doc.setFont("times", "italic");
    doc.text(`Analysis Date: ${currentDate}`, 10, 20);

    //fit score 
    doc.setFontSize(16);
    doc.setFont("times", "bold");
    doc.text("Fit Score:", 10, 40);
    doc.setFontSize(16);
    doc.setFont("times", "bold");

    // Set color to red or green depending on whether it is above or below 50
    if (fitScore > 50) {
        doc.setTextColor(0, 128, 0); // Green
    } else {
        doc.setTextColor(255, 0, 0); // Red
    }

    doc.text(`${fitScore}%`, 50, 40);

    //keyword placement 
    doc.setFontSize(16);
    doc.setFont("times", "bold");
    doc.text("Matched Keywords:", 10, 70);
    doc.setFontSize(14);
    doc.setFont("times", "normal");
    doc.setTextColor(0, 128, 0); 
    matchedKeywords.forEach((keyword, index) => {
        doc.text(`- ${keyword}`, 15, 80 + index * 8);
    });
    doc.setTextColor(0);

    //feedback
    const feedbackStartY = 90 + matchedKeywords.length * 8;
    doc.setFontSize(16);
    doc.setFont("times", "bold");
    doc.text("Feedback:", 10, feedbackStartY);
    doc.setFontSize(14);
    doc.setFont("times", "normal");
    feedback.forEach((item, index) => {
        const feedbackY = feedbackStartY + 10 + index * 8;
        doc.text(`- ${item}`, 15, feedbackY);
    });

    //footer
    const footerText = "Jeremy Kurian, Ari Kamat, Safwan Noor, Haitham Awad, Noah Paul\nTeam TBD";
    doc.setFontSize(10);
    doc.setFont("times", "normal");
    doc.text(footerText, 105, 280, { align: 'center' });

    const formattedDate = currentDate.replace(/\//g, '-'); 
    doc.save(`resume_report_${formattedDate}.pdf`);
}
