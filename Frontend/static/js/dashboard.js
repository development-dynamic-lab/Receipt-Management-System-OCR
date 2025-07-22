document.addEventListener('DOMContentLoaded', function () {
    // ===== Element Selections ===== //
    const fileInput = document.getElementById('imageUpload');
    const uploadButton = document.querySelector('.upload-button');
    const previewContainer = document.querySelector('.image-area');
    const imageTitle = document.querySelector('.image-head');
    const back = document.querySelector('.back');
    const userDisplayElement = document.querySelector('.login-name');
    const analyze = document.querySelector('.analyze-button');
    const markdownArea = document.querySelector('.markdown-area');
    const userName = localStorage.getItem('loginName');
    const askAI = document.querySelector('.ask-ai-button');

    
    // =============== Go to ask ai =============//
    askAI.addEventListener('click', () => {
        window.location.href = '/agent'; 
    });
    

    // ===== Display Logged-In Username ===== //
    if (userName && userDisplayElement) {
        userDisplayElement.innerHTML = `<span style="font-size: 2rem;">👤</span> ${userName}`;
    }

    // ===== Back Button Click: Go to Home Page ===== //
    back.addEventListener('click', function () {
        window.location.href = '/';
    });

    // ===== Trigger File Input on Upload Button Click ===== //
    uploadButton.addEventListener('click', function () {
        fileInput.click();
    });

    let formData = new FormData(); // Used to store selected files

    // ===== Handle File Input Change ===== //
    fileInput.addEventListener('change', function () {
        imageTitle.style.display = 'block'; // Show heading
        document.querySelectorAll('.preview-image-container').forEach(el => el.remove()); // Remove previous previews
        formData = new FormData(); // Reset form data

        Array.from(fileInput.files).forEach((file, index) => {
            if (file.type.startsWith('image/')) {
                formData.append('images', file); // Add file to formData
                const reader = new FileReader();

                reader.onload = function (e) {
                    // Create preview container for each image
                    const imageContainer = document.createElement('div');
                    imageContainer.classList.add('preview-image-container');
                    imageContainer.style.marginBottom = '10px';

                    // Add label above each preview
                    const receiptLabel = document.createElement('h3');
                    receiptLabel.textContent = `Receipt ${index + 1}`;
                    receiptLabel.style.textAlign = 'center';
                    receiptLabel.style.marginBottom = '5px';
                    receiptLabel.style.color = 'red';

                    // Create preview div
                    const imageDiv = document.createElement('div');
                    imageDiv.classList.add('preview-image');
                    imageDiv.style.backgroundImage = `url('${e.target.result}')`;

                    // Append to DOM
                    imageContainer.appendChild(receiptLabel);
                    imageContainer.appendChild(imageDiv);
                    previewContainer.appendChild(imageContainer);
                };
                reader.readAsDataURL(file); // Read image file
            }
        });
    });

    // ===== Handle Analyze Button Click ===== //
    if (analyze) {
        analyze.addEventListener('click', async function () {
            const allAnalysis = await uploadImages(formData); // Upload and analyze images

            if (allAnalysis && Array.isArray(allAnalysis)) {
                const chatHead = markdownArea.querySelector('.chat-head');
                const loader = markdownArea.querySelector('.markdown-loader');

                // Clear old responses
                markdownArea.querySelectorAll('.receipt-response').forEach(el => el.remove());

                // Append loading UI if needed
                if (chatHead && !markdownArea.contains(chatHead)) {
                    markdownArea.appendChild(chatHead);
                }

                if (loader && !markdownArea.contains(loader)) {
                    markdownArea.appendChild(loader);
                }

                // Render results
                allAnalysis.forEach((data, index) => {
                    const responseDiv = document.createElement('div');
                    responseDiv.classList.add('receipt-response');

                    // Handle error cases
                    if (data === "Oops! Something wrong!!" || data === "wrong_image") {
                        const bubuCryingGif = document.createElement('img');
                        bubuCryingGif.src = 'https://media.tenor.com/sWXhCC4A2woAAAAj/bubu-bubu-dudu.gif';
                        bubuCryingGif.alt = 'Bubu crying';
                        bubuCryingGif.style.width = '150px';

                        const errorMessage = document.createElement('p');
                        if (data === "Oops! Something wrong!!") {
                            errorMessage.textContent = `Oops! Something went wrong while processing Receipt ${index + 1}.`;
                        } else if (data === "wrong_image") {
                            errorMessage.textContent = `The uploaded image for Receipt  ${index + 1} is not a Japanese receipt.`;
                        }
                        errorMessage.style.color = 'red';
                        errorMessage.style.fontWeight = 'bold';

                        responseDiv.appendChild(bubuCryingGif);
                        responseDiv.appendChild(errorMessage);
                    } else {
                        // Generate receipt tables
                        const tableElements = createReceiptTables(data, index);
                        tableElements.forEach(el => responseDiv.appendChild(el));
                    }

                    markdownArea.appendChild(responseDiv); // Add to output area
                });
            }
        });
    }
});

// ===== Upload Image to Server and Return Analysis ===== //
async function uploadImages(formData) {
    const markdownArea = document.querySelector('.markdown-area');
    const loader = markdownArea.querySelector('.markdown-loader');

    try {
        console.log('Uploading images...');
        alert('Images uploaded successfully! Analysis starting...');

        markdownArea.querySelectorAll('.receipt-response').forEach(el => el.remove()); // Clear old

        if (loader) loader.style.display = 'flex'; // Show loading

        const response = await fetch('/api/upload-images', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (loader) loader.style.display = 'none'; // Hide loading

        // Handle success
        if (result.status === 'success') {
            alert('Analysis completed!');
            return result.all_analysis;
        } else {
            // Handle error when user uploads more than allowed images
            const responseDiv = document.createElement('div');
            responseDiv.classList.add('receipt-response');

            const bubuCryingGif = document.createElement('img');
            bubuCryingGif.src = 'https://media.tenor.com/qeCBPb-oz5cAAAAj/bubu-crying-bubu-no-no.gif';
            bubuCryingGif.alt = 'Bubu crying';
            bubuCryingGif.style.width = '150px';

            const errorMessage = document.createElement('p');
            errorMessage.textContent = 'You can only upload up to 5 receipts for analysis.';
            errorMessage.style.color = 'red';

            responseDiv.appendChild(bubuCryingGif);
            responseDiv.appendChild(errorMessage);
            markdownArea.appendChild(responseDiv);
        }
    } catch (error) {
        console.error('Error uploading images:', error);
        if (loader) loader.style.display = 'none';
    }
}

// ===== Generate Both Japanese and English Receipt Tables ===== //
function createReceiptTables(data, index) {
    const elements = [];

    const receiptHeading = document.createElement('h2');
    receiptHeading.textContent = `Receipt ${index + 1}`;
    receiptHeading.style.color = 'red';
    receiptHeading.style.textAlign = 'center';
    elements.push(receiptHeading);

    const outerTableStyle = {
        width: '100%',
        tableLayout: 'fixed',
        borderCollapse: 'collapse',
        marginBottom: '20px'
    };

    const headings = ['Date', 'Store Name', 'Items Bought', 'Total Amount', 'Payment Method', 'Consumption Tax'];
    const japaneseHeadings = ['日付', '店舗名', '購入品目', '合計金額', '支払方法', '消費税'];
    const columnWidths = ['11%', '11%', '44%', '11%', '11%', '12%'];

    function createTable(titleText, titleColor, headingLabels, rowData, langKey) {
        const title = document.createElement('h3');
        title.textContent = titleText;
        title.style.color = titleColor;

        const table = document.createElement('table');
        Object.assign(table.style, outerTableStyle);

        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');

        // Create header row
        headingLabels.forEach((label, idx) => {
            const th = document.createElement('th');
            th.textContent = label;
            th.style.width = columnWidths[idx];
            th.style.border = '1px solid black';
            th.style.padding = '6px';
            th.style.wordBreak = 'break-word';
            th.style.textAlign = 'center';
            headerRow.appendChild(th);
        });

        thead.appendChild(headerRow);
        table.appendChild(thead);

        // Create single data row
        const row = document.createElement('tr');
        const cells = [
            rowData['Date'],
            rowData['Store Name'],
            generateItemsTable(data['Itemized List'], langKey),
            rowData['Total Amount'],
            rowData['Payment Method'],
            rowData['Consumption Tax']
        ];

        cells.forEach(cell => {
            const td = document.createElement('td');
            td.style.border = '1px solid black';
            td.style.padding = '6px';
            td.style.wordBreak = 'break-word';
            td.style.verticalAlign = 'top';

            // Handle embedded tables
            if (cell instanceof HTMLElement) {
                const wrapper = document.createElement('div');
                wrapper.style.display = 'flex';
                wrapper.style.justifyContent = 'center';
                td.appendChild(wrapper);
                wrapper.appendChild(cell);
            } else {
                td.textContent = cell;
            }

            row.appendChild(td);
        });

        const tbody = document.createElement('tbody');
        tbody.appendChild(row);
        table.appendChild(tbody);

        return [title, table];
    }

    // Japanese and English Tables
    elements.push(...createTable('日本語の領収書', 'green', japaneseHeadings, {
        'Date': data['Date'][1],
        'Store Name': data['Store Name'][1],
        'Total Amount': data['Total Amount'][1],
        'Payment Method': data['Payment Method'][1],
        'Consumption Tax': data['Consumption Tax'][1]
    }, 'japaneseName'));

    elements.push(...createTable('Receipt (English)', '#007BFF', headings, {
        'Date': data['Date'][0],
        'Store Name': data['Store Name'][0],
        'Total Amount': data['Total Amount'][0],
        'Payment Method': data['Payment Method'][0],
        'Consumption Tax': data['Consumption Tax'][0]
    }, 'englishName'));

    return elements;
}

// ===== Create Itemized Table for Each Receipt ===== //
function generateItemsTable(items, langKey) {
    const table = document.createElement('table');

    Object.assign(table.style, {
        width: '95%',
        borderCollapse: 'collapse',
        fontSize: '0.95rem',
        backgroundColor: '#fefefe'
    });

    const headers = langKey === 'englishName'
        ? ['Item Name', 'Quantity', 'Unit Price', 'Total Price']
        : ['品目名', '数量', '単価', '合計金額'];

    // Create header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    headers.forEach(h => {
        const th = document.createElement('th');
        th.textContent = h;
        Object.assign(th.style, {
            padding: '6px',
            border: '1px solid black',
            textAlign: 'center'
        });
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create item rows
    const tbody = document.createElement('tbody');
    items.forEach(item => {
        const row = document.createElement('tr');
        const name = item[langKey];
        const qty = item.quantity;
        const unit = `¥${item.unitPrice.toLocaleString()}`;
        const total = `¥${item.totalPrice.toLocaleString()}`;

        [name, qty, unit, total].forEach(val => {
            const td = document.createElement('td');
            td.textContent = val;
            Object.assign(td.style, {
                padding: '6px',
                border: '1px solid black',
                wordBreak: 'break-word',
                textAlign: 'center'
            });
            row.appendChild(td);
        });

        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    return table;
}
