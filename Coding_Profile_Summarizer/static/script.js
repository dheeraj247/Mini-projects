document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('profile-form');
    const resultsContainer = document.getElementById('results-container');
    const loadingIndicator = document.getElementById('loading-indicator');
    const fetchBtn = document.getElementById('fetch-btn');
    const fetchBtnText = fetchBtn.querySelector('.btn-text');
    const fetchBtnIcon = fetchBtn.querySelector('.btn-icon');
    const originalBtnText = fetchBtnText.innerHTML;
    const originalBtnIconHTML = fetchBtnIcon.innerHTML;
    
    const platformLogos = {
        leetcode: 'https://assets.leetcode.com/static_assets/public/images/LeetCode_logo_rvs.png',
        codechef: 'https://cdn.brandfetch.io/idM2-b7Taf/w/400/h/400/theme/dark/icon.jpeg?c=1dxbfHSJFAPEGdCLU4o5B',
        gfg: 'https://media.geeksforgeeks.org/wp-content/cdn-uploads/gfg_200x200-min.png',
        hackerrank: 'https://hrcdn.net/fcore/assets/work/header/hackerrank_logo-21e2867566.svg'
    };
    const platformDefaultIcons = {
        leetcode: 'fa-solid fa-keyboard',
        codechef: 'fa-solid fa-utensils',
        gfg: 'fa-solid fa-graduation-cap',
        hackerrank: 'fa-solid fa-medal'
    };
    
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        resultsContainer.innerHTML = ''; 
        loadingIndicator.style.display = 'flex';
        
        fetchBtn.disabled = true;
        fetchBtnText.textContent = 'Fetching...';
        fetchBtnIcon.innerHTML = '<div class="spinner-btn"></div>';
    
        const platform = document.getElementById('platform').value;
        const usernameInput = document.getElementById('username').value.trim();
    
        if (!usernameInput) {
            displayError("Username cannot be empty.");
            resetFetchButton();
            loadingIndicator.style.display = 'none';
            return;
        }
    
        try {
            const response = await fetch('/api/fetch_profile_data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ platform, username: usernameInput }),
            });
    
            const data = await response.json();
    
            if (data.error) {
                displayError(data.error);
            } else {
                
                displayData(platform, usernameInput, data);
            }
        } catch (error) {
            console.error("Fetch error:", error);
            displayError('An error occurred while fetching data. Check the console or network tab for details.');
        } finally {
            loadingIndicator.style.display = 'none';
            resetFetchButton();
        }
    });
    
    function resetFetchButton() {
        fetchBtn.disabled = false;
        fetchBtnText.textContent = originalBtnText;
        fetchBtnIcon.innerHTML = originalBtnIconHTML;
    }
    
    function displayError(message) {
        resultsContainer.innerHTML = `<div class="error-message"><i class="fas fa-exclamation-triangle"></i> ${message}</div>`;
    }
    
    function sanitizeValue(value, label = "") {
        const naValues = [
            "n/a", "na", "not found", "no rating available", "not available", 
            null, undefined, ""
        ];
        if (typeof value === 'string' && naValues.includes(value.toLowerCase())) {
            return '<span class="value na">N/A</span>';
        }
        if (typeof value === 'number' && value === 0 && 
            (label.toLowerCase().includes("rank") || label.toLowerCase().includes("rating")) && 
            !label.toLowerCase().includes("solved")) {
             return '<span class="value na">N/A</span>'; // Treat 0 rank/rating as N/A unless it's a count
        }
        return `<span class="value">${value}</span>`;
    }
    
    function createProfileItemHTML(iconClass, label, value) {
        const displayValue = sanitizeValue(value, label);
        return `<div class="profile-item">
                    <i class="item-icon ${iconClass}"></i>
                    <strong>${label}:</strong> 
                    ${displayValue}
                </div>`;
    }
    
    function displayData(platform, queryUsername, data) {
        let cardContent = `<div class="profile-card">`;
        
        const platformLogoUrl = platformLogos[platform];
        const platformIconClass = platformDefaultIcons[platform];
        
        
        const displayUsername = data.username || queryUsername;
    
        // Card Header
        cardContent += `<div class="profile-card-header">`;
        if (platformLogoUrl) {
            cardContent += `<img src="${platformLogoUrl}" alt="${platform} logo" class="platform-logo">`;
        } else if (platformIconClass) { // Fallback icon if logo URL is missing
             cardContent += `<i class="${platformIconClass} platform-logo" style="font-size: 2.5em; color: var(--primary-color);"></i>`;
        }
        
        cardContent += `<div class="profile-card-header-info">
                          <h2><span class="username-highlight">${displayUsername}</span></h2>`;

        cardContent += `  </div>
                       </div>`; // End profile-card-header
    

        cardContent += `<div class="profile-grid">`;
    
        switch (platform) {
            case 'codechef':
                cardContent += createProfileItemHTML('fas fa-star', 'Rating', data.rating);
                cardContent += createProfileItemHTML('fas fa-medal', 'Stars', data.stars);
                cardContent += createProfileItemHTML('fas fa-layer-group', 'Division', data.division);
                cardContent += createProfileItemHTML('fas fa-arrow-trend-up', 'Highest Rating', data.highest_rating);
                cardContent += createProfileItemHTML('fas fa-globe', 'Global Rank', data.global_rank);
                cardContent += createProfileItemHTML('fas fa-flag', 'Country Rank', data.country_rank);
                cardContent += createProfileItemHTML('fas fa-check-circle', 'Problems Solved', data.solved_problems);
                break;
            case 'gfg':
                cardContent += createProfileItemHTML('fas fa-trophy', 'Coding Score', data.coding_score);
                cardContent += createProfileItemHTML('fas fa-ranking-star', 'Rank', data.rank);
                cardContent += createProfileItemHTML('fas fa-puzzle-piece', 'Problems Solved', data.problems_solved);
                cardContent += createProfileItemHTML('fas fa-university', 'Institution', data.institution);
                cardContent += createProfileItemHTML('fas fa-star-half-alt', 'Contest Rating', data.contest_rating);
                break;
            case 'hackerrank':
                cardContent += createProfileItemHTML('fas fa-user-tag', 'Profile For', displayUsername);
                break;
            case 'leetcode':
                cardContent += createProfileItemHTML('fas fa-poll', 'Reputation/Rating', data.rating);
                cardContent += createProfileItemHTML('fas fa-ranking-star', 'Global Rank', data.rank);
                cardContent += createProfileItemHTML('fas fa-tasks', 'Total Solved', data.solved);
                break;
        }
        cardContent += `</div>`; // End profile-grid
    
        // List sections for additional data
        let listSectionsHTML = "";
    
        if (platform === 'gfg' && data.difficulty_counts && Object.keys(data.difficulty_counts).length > 0) {
            const validCounts = Object.entries(data.difficulty_counts).filter(([, count]) => parseInt(count) > 0);
            if (validCounts.length > 0) {
                listSectionsHTML += `<div class="list-section difficulty-counts"><h4><i class="fas fa-chart-pie"></i>Difficulty Counts:</h4><ul>`;
                validCounts.forEach(([difficulty, count]) => {
                    listSectionsHTML += `<li>${difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}: <strong>${count}</strong></li>`;
                });
                listSectionsHTML += `</ul></div>`;
            }
        }
    
        if (platform === 'hackerrank') {
            if (data.badges && data.badges.length > 0) {
                listSectionsHTML += `<div class="list-section badges-list"><h4><i class="fas fa-award"></i> Badges:</h4><ul>`;
                data.badges.forEach(badge => {
                    listSectionsHTML += `<li class="badge-item">
                        <span class="badge-title">${badge.title || 'Unknown'}</span>
                        ${badge.stars > 0 ? `<span class="badge-stars">${'★'.repeat(badge.stars)}</span>` : ''}
                        ${badge.level && badge.level !== 'Unknown' ? `<span class="badge-level">(${badge.level})</span>` : ''}
                    </li>`;
                });
                listSectionsHTML += `</ul></div>`;
            }
            if (data.certificates && data.certificates.length > 0) {
                listSectionsHTML += `<div class="list-section certificates-list"><h4><i class="fas fa-certificate"></i> Certificates:</h4><ul>`;
                data.certificates.forEach(cert => {
                    listSectionsHTML += `<li class="certificate-item">${cert}</li>`;
                });
                listSectionsHTML += `</ul></div>`;
            }
             if (listSectionsHTML === "" && !(data.badges && data.badges.length > 0) && !(data.certificates && data.certificates.length > 0)){
                listSectionsHTML = `<p style="text-align:center; color: var(--light-text-color); margin-top: 20px;">No badges or certificates found for this user.</p>`;
            }
        }
        
        if (platform === 'leetcode') {
            if (data.difficulty && Object.keys(data.difficulty).length > 0) {
                 const validDifficulties = Object.entries(data.difficulty).filter(([, count]) => count > 0);
                 if (validDifficulties.length > 0) {
                    listSectionsHTML += `<div class="list-section difficulty-counts"><h4><i class="fas fa-tachometer-alt"></i>Solved by Difficulty:</h4><ul>`;
                    validDifficulties.forEach(([difficulty, count]) => {
                        listSectionsHTML += `<li>${difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}: <strong>${count}</strong></li>`;
                    });
                    listSectionsHTML += `</ul></div>`;
                 }
            }
            if (data.languageStats && Object.keys(data.languageStats).length > 0) {
                listSectionsHTML += `<div class="list-section language-stats"><h4><i class="fas fa-code"></i>Language Stats:</h4><ul>`;
                const sortedLangs = Object.entries(data.languageStats).sort(([,a],[,b]) => b-a); // Sort by problems solved desc
                sortedLangs.forEach(([language, count]) => {
                    listSectionsHTML += `<li>${language}: <strong>${count}</strong></li>`;
                });
                listSectionsHTML += `</ul></div>`;
            }
        }
        
        cardContent += listSectionsHTML;
        cardContent += `</div>`; // Close profile-card
        resultsContainer.innerHTML = cardContent;
    }
    });