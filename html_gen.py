import json

# Path to the JSON file containing the URLs
json_file_path = 'non_quick_apply_urls.json'
html_file_path = 'job_postings.html'

# Read the JSON file to get the URLs
with open(json_file_path, 'r') as json_file:
    non_quick_apply_urls = json.load(json_file)

# Generate HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Non-Quick Apply Job URLs</title>
    <style>
        .visited {
            color: green;
            font-weight: bold;
        }
        .not-visited {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Non-Quick Apply Job Postings</h1>
    <ul id="job-list">
"""

# Add each URL to the HTML content
for url in non_quick_apply_urls:
    html_content += f"""
        <li id="job-{url}">
            <a href="{url}" target="_blank" class="job-link">{url}</a>
            <span class="status"></span>
        </li>
    """

# Closing the list and the rest of the HTML content
html_content += """
    </ul>

    <script>
        // Fetch all job URLs and check if they've been visited
        document.querySelectorAll('.job-link').forEach(function(link) {
            const url = link.href;
            const statusSpan = link.nextElementSibling;

            // Check if the URL has been visited by looking in localStorage
            const visited = localStorage.getItem(url) === 'true';

            if (visited) {
                statusSpan.textContent = " - Visited";
                statusSpan.classList.add('visited');
            } else {
                statusSpan.textContent = " - Not Visited";
                statusSpan.classList.add('not-visited');
            }

            // Add click event to mark as visited
            link.addEventListener('click', function() {
                localStorage.setItem(url, 'true');  // Mark the URL as visited
                statusSpan.textContent = " - Visited";
                statusSpan.classList.remove('not-visited');
                statusSpan.classList.add('visited');
            });
        });
    </script>
</body>
</html>
"""

# Write the HTML content to a file
with open(html_file_path, 'w') as html_file:
    html_file.write(html_content)

print(f"HTML file with job URLs has been generated and saved as '{html_file_path}'.")
