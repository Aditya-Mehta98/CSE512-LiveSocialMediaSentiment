document.addEventListener("DOMContentLoaded", function () {
    const analyzeButton = document.getElementById('analyzeButton');

    analyzeButton.addEventListener('click', async () => {
        const keyword = document.getElementById('searchKeyword').value;

        if (!keyword) {
            alert("Please enter a keyword to analyze.");
            return;
        }

        // Send keyword to back-end to start analysis
        try {
            const response = await fetch("http://localhost:5000/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ keyword })
            });
            if (response.ok) {
                const data = await response.json();
                displayChart(data);
            } else {
                console.error("Error starting sentiment analysis");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });

    function displayChart(sentimentCounts) {
        const ctx = document.getElementById('sentimentChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [sentimentCounts.positive, sentimentCounts.neutral, sentimentCounts.negative],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(255, 205, 86, 0.2)',
                        'rgba(255, 99, 132, 0.2)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Live YouTube Sentiment Analysis'
                    }
                }
            }
        });
    }
});
