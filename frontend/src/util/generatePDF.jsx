import jsPDF from "jspdf";
//task 26 a lot of hard coding
export function generatePDF(
  fitScore,
  matchedKeywords,
  missingKeywords,
  improvementSuggestions,
) {
  const doc = new jsPDF();
  const currentDate = new Date().toLocaleDateString();
  doc.setFontSize(16);
  doc.setFont("times", "bold");
  doc.text("Resume Analysis Report", 105, 10, {
    align: "center",
    underline: true,
  });
  doc.setFontSize(10);
  doc.setFont("times", "italic");
  doc.text(`Analysis Date: ${currentDate}`, 10, 20);

  doc.setFontSize(14);
  doc.setFont("times", "bold");
  doc.text("Fit Score:", 10, 30);

  if (fitScore > 50) {
    doc.setTextColor(0, 128, 0);
  } else {
    doc.setTextColor(255, 0, 0);
  }
  doc.text(`${fitScore.toFixed(2)}%`, 50, 30);
  doc.setTextColor(0);

  doc.setFontSize(14);
  doc.setFont("times", "bold");
  doc.text("Matched Keywords:", 10, 45);
  doc.setFontSize(10);
  doc.setFont("times", "normal");

  let currentY = 55;
  Object.keys(matchedKeywords).forEach((category) => {
    doc.text(
      `${category.charAt(0).toUpperCase() + category.slice(1)}:`,
      15,
      currentY,
    );
    currentY += 6;
    matchedKeywords[category].forEach((keyword) => {
      const wrappedText = doc.splitTextToSize(`- ${keyword}`, 180);
      doc.text(wrappedText, 20, currentY);
      currentY += wrappedText.length * 6;
    });
  });

  currentY += 10;
  doc.setFontSize(14);
  doc.setFont("times", "bold");
  doc.text("Missing Keywords:", 10, currentY);
  currentY += 10;
  doc.setFontSize(10);
  doc.setFont("times", "normal");
  Object.keys(missingKeywords).forEach((category) => {
    doc.text(
      `${category.charAt(0).toUpperCase() + category.slice(1)}:`,
      15,
      currentY,
    );
    currentY += 6;
    missingKeywords[category].forEach((keyword) => {
      const wrappedText = doc.splitTextToSize(`- ${keyword}`, 180);
      doc.text(wrappedText, 20, currentY);
      currentY += wrappedText.length * 6;
    });
  });

  //new page cause might be too many skills
  doc.addPage();
  currentY = 10;
  doc.setFontSize(14);
  doc.setFont("times", "bold");
  doc.text("Improvement Suggestions:", 10, currentY);
  currentY += 10;
  doc.setFontSize(9);
  doc.setFont("times", "normal");
  Object.keys(improvementSuggestions).forEach((category) => {
    doc.text(
      `${category.charAt(0).toUpperCase() + category.slice(1)}:`,
      15,
      currentY,
    );
    currentY += 6;
    Object.keys(improvementSuggestions[category]).forEach((keyword) => {
      const wrappedText = doc.splitTextToSize(
        `- ${keyword}: ${improvementSuggestions[category][keyword]}`,
        180,
      );
      doc.text(wrappedText, 20, currentY);
      currentY += wrappedText.length * 6;
    });
  });

  const footerText =
    "Jeremy Kurian, Ari Kamat, Safwan Noor, Haitham Awad, Noah Paul\nTeam TBD";
  doc.setFontSize(8);
  doc.setFont("times", "normal");
  doc.text(footerText, 105, 280, { align: "center" });
  const formattedDate = currentDate.replace(/\//g, "-");
  doc.save(`resume_report_${formattedDate}.pdf`);
}
