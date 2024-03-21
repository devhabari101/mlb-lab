        // Fetch JSON data from the server
        fetch('markdown_output.json')
            .then(response => response.json())
            .then(data => {
                // Get the div element to display the markdown content
                const markdownContentDiv = document.getElementById('markdown-content');

                // Iterate over each item in the JSON data
                data.forEach(item => {
                    // Create elements for title and content
                    const titleElement = document.createElement('h2');
                    const contentElement = document.createElement('div');

                    // Set title text
                    titleElement.textContent = item.metadata.title;

                    // Set content HTML
                    contentElement.innerHTML = item.content;

                    // Append title and content to the markdownContentDiv
                    markdownContentDiv.appendChild(titleElement);
                    markdownContentDiv.appendChild(contentElement);
                });
            })
            .catch(error => console.error('Error fetching JSON:', error));
    
