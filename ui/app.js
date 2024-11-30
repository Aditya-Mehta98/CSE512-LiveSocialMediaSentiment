document.getElementById("analyzeButton").addEventListener("click", function() {
    const keyword = document.getElementById("searchKeyword").value.trim();
    if (!keyword) {
        alert("Please enter a keyword to analyze.");
        return;
    }

    // Reset results
    document.getElementById("videoDetails").style.display = "none";
    document.getElementById("results").style.display = "none";
    const videoDetails = document.getElementById("videoDetails");
    videoDetails.innerHTML = "";
    const summary = document.getElementById("summary");
    summary.innerHTML = "";

    document.getElementById("loading").style.display = "block";

    // Fetch the new analysis data
    fetch('/analyze_video', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keyword }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loading").style.display = "none";

        if (!data || data.analyzed_data.length === 0) {
            alert("No data found for the given keyword. Please try another.");
            return;
        }

        document.getElementById("videoDetails").style.display = "block";

        // Display details for the top 10 videos only
        data.analyzed_data.forEach(video => {
            const videoInfo = `
                <div class="card mb-3">
                    <div class="card-body">
                        <h3><a href="${video.url}" target="_blank">${video.title}</a></h3>
                        <p>Views: ${video.popularity_metrics.view_count}, Likes: ${video.popularity_metrics.like_count}, Comments: ${video.popularity_metrics.comment_count}</p>
                        <p><strong>Sentiment:</strong> ${video.sentiment}</p>
                        <p><strong>Detected Entities:</strong> ${video.entities.length ? video.entities.join(", ") : "None"}</p>
                    </div>
                </div>
            `;
            videoDetails.innerHTML += videoInfo;
        });

        // Use all 50 videos to compute sentiment counts
        const sentimentCounts = {};
        data.summary_data.forEach(video => {
            const sentiment = capitalizeFirstLetter(video.sentiment);
            sentimentCounts[sentiment] = (sentimentCounts[sentiment] || 0) + 1;
        });

        // Display only sentiments that are present in the analysis
        document.getElementById("results").style.display = "flex";

        // Calculate percentage stats and display a summary
        const totalVideos = data.summary_data.length;
        let summaryText = "<p>Sentiment Summary:</p><ul>";
        for (const [sentiment, count] of Object.entries(sentimentCounts)) {
            const percentage = ((count / totalVideos) * 100).toFixed(2);
            summaryText += `<li>${sentiment}: ${count} videos (${percentage}%)</li>`;
        }
        summaryText += "</ul>";
        summary.innerHTML = summaryText;

        // Create pie chart with only sentiments that are present
        const ctx = document.getElementById('sentimentChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: Object.keys(sentimentCounts),
                datasets: [{
                    label: 'Sentiment Analysis',
                    data: Object.values(sentimentCounts),
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(153, 102, 255, 0.6)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                const total = tooltipItem.dataset.data.reduce((acc, val) => acc + val, 0);
                                const percentage = ((tooltipItem.raw / total) * 100).toFixed(2);
                                return `${tooltipItem.label}: ${tooltipItem.raw} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("loading").style.display = "none";
    });
});

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}
