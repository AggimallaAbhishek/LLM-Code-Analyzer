// LLM Code Analyzer - Frontend JavaScript

const API_BASE = '/api';

// Sample vulnerable code for demo
const SAMPLE_CODE = `# Example vulnerable Python code
import os
import pickle

def get_user(user_id):
    # SQL Injection vulnerability
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    result = db.execute(query)
    return result

def run_command(cmd):
    # Command injection vulnerability
    os.system("echo " + cmd)

def process_data(data):
    # Insecure deserialization
    obj = pickle.loads(data)
    return obj

# Hardcoded credentials
API_KEY = "sk-1234567890abcdef"
PASSWORD = "admin123"

def dangerous_eval(user_input):
    # Arbitrary code execution
    result = eval(user_input)
    return result
`;

// DOM Elements
const codeInput = document.getElementById('code-input');
const languageSelect = document.getElementById('language-select');
const analyzeBtn = document.getElementById('analyze-btn');
const clearBtn = document.getElementById('clear-btn');
const sampleBtn = document.getElementById('sample-btn');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');
const errorMessage = document.getElementById('error-message');
const llmModeSpan = document.getElementById('llm-mode');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchConfig();
    setupEventListeners();
});

function setupEventListeners() {
    analyzeBtn.addEventListener('click', analyzeCode);
    clearBtn.addEventListener('click', clearAll);
    sampleBtn.addEventListener('click', loadSample);
    
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });
}

async function fetchConfig() {
    try {
        const response = await fetch(`${API_BASE}/config`);
        const config = await response.json();
        llmModeSpan.textContent = `Mode: ${config.llm_mode} (${config.model})`;
    } catch (error) {
        llmModeSpan.textContent = 'Mode: Unknown';
    }
}

async function analyzeCode() {
    const code = codeInput.value.trim();
    if (!code) {
        showError('Please enter some code to analyze.');
        return;
    }

    setLoading(true);
    hideResults();
    hideError();

    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: code,
                language: languageSelect.value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Analysis failed');
        }

        if (!data.success) {
            throw new Error(data.error || 'Analysis failed');
        }

        displayResults(data);
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

function displayResults(data) {
    resultsSection.classList.remove('hidden');
    
    // Risk Score
    const riskScore = document.getElementById('risk-score');
    riskScore.textContent = data.risk_score;
    riskScore.className = 'risk-score ' + getRiskClass(data.risk_score);
    
    // Summary
    document.getElementById('summary').textContent = data.summary;
    
    // Update counts
    document.getElementById('vuln-count').textContent = data.vulnerabilities?.length || 0;
    document.getElementById('surface-count').textContent = data.attack_surfaces?.length || 0;
    document.getElementById('boundary-count').textContent = data.trust_boundaries?.length || 0;
    
    // Store data for tab switching
    window.analysisData = data;
    
    // Show vulnerabilities tab by default
    switchTab('vulnerabilities');
}

function switchTab(tabName) {
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    
    const content = document.getElementById('tab-content');
    const data = window.analysisData;
    
    if (!data) return;
    
    switch (tabName) {
        case 'vulnerabilities':
            content.innerHTML = renderVulnerabilities(data.vulnerabilities || []);
            break;
        case 'attack-surfaces':
            content.innerHTML = renderAttackSurfaces(data.attack_surfaces || []);
            break;
        case 'trust-boundaries':
            content.innerHTML = renderTrustBoundaries(data.trust_boundaries || []);
            break;
        case 'recommendations':
            content.innerHTML = renderRecommendations(data.recommendations || []);
            break;
    }
}

function renderVulnerabilities(vulns) {
    if (vulns.length === 0) {
        return '<p style="color: var(--success-color); text-align: center; padding: 2rem;">✅ No vulnerabilities detected!</p>';
    }
    
    return vulns.map(v => `
        <div class="vuln-card">
            <div class="vuln-header">
                <span class="vuln-type">${escapeHtml(v.type)}</span>
                <span class="severity-badge ${v.severity}">${v.severity}</span>
            </div>
            <p class="vuln-description">${escapeHtml(v.description)}</p>
            ${v.line_numbers?.length ? `<p class="vuln-line">📍 Lines: ${v.line_numbers.join(', ')}</p>` : ''}
            ${v.vulnerable_code ? `
                <p class="code-label">Vulnerable Code:</p>
                <pre class="code-block vulnerable">${escapeHtml(v.vulnerable_code)}</pre>
            ` : ''}
            <div class="fix-suggestion">
                <strong>💡 Fix:</strong> ${escapeHtml(v.fix_suggestion)}
            </div>
            ${v.fixed_code ? `
                <p class="code-label">Fixed Code:</p>
                <pre class="code-block fixed">${escapeHtml(v.fixed_code)}</pre>
            ` : ''}
        </div>
    `).join('');
}

function renderAttackSurfaces(surfaces) {
    if (surfaces.length === 0) {
        return '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No attack surfaces identified.</p>';
    }
    
    return surfaces.map(s => `
        <div class="surface-card">
            <div class="surface-header">
                <span class="surface-name"><strong>${escapeHtml(s.name)}</strong></span>
                <span class="risk-level ${s.risk_level}">${s.risk_level}</span>
            </div>
            <span class="surface-type">${escapeHtml(s.type)}</span>
            <p style="margin-top: 0.5rem; color: var(--text-secondary);">${escapeHtml(s.description)}</p>
        </div>
    `).join('');
}

function renderTrustBoundaries(boundaries) {
    if (boundaries.length === 0) {
        return '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No trust boundaries identified.</p>';
    }
    
    return boundaries.map(b => `
        <div class="boundary-card">
            <div class="boundary-header">
                <span class="boundary-name"><strong>🔐 ${escapeHtml(b.name)}</strong></span>
            </div>
            <p style="color: var(--text-secondary);">${escapeHtml(b.description)}</p>
            ${b.components?.length ? `
                <p style="margin-top: 0.5rem; font-size: 0.9rem;">
                    Components: ${b.components.map(c => `<code>${escapeHtml(c)}</code>`).join(', ')}
                </p>
            ` : ''}
        </div>
    `).join('');
}

function renderRecommendations(recs) {
    if (recs.length === 0) {
        return '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No additional recommendations.</p>';
    }
    
    return `<ul class="recommendation-list">
        ${recs.map(r => `<li>${escapeHtml(r)}</li>`).join('')}
    </ul>`;
}

function getRiskClass(score) {
    if (score >= 75) return 'critical';
    if (score >= 50) return 'high';
    if (score >= 25) return 'medium';
    return 'low';
}

function setLoading(isLoading) {
    analyzeBtn.disabled = isLoading;
    document.querySelector('.btn-text').classList.toggle('hidden', isLoading);
    document.querySelector('.spinner').classList.toggle('hidden', !isLoading);
}

function showError(message) {
    errorSection.classList.remove('hidden');
    errorMessage.textContent = message;
}

function hideError() {
    errorSection.classList.add('hidden');
}

function hideResults() {
    resultsSection.classList.add('hidden');
}

function clearAll() {
    codeInput.value = '';
    hideResults();
    hideError();
    window.analysisData = null;
}

function loadSample() {
    codeInput.value = SAMPLE_CODE;
    languageSelect.value = 'python';
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
