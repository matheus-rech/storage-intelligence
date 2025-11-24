// Storage Intelligence - Renderer Script
class StorageIntelligenceApp {
    constructor() {
        this.currentPage = 'dashboard';
        this.currentAnalysis = null;
        this.isAnalyzing = false;

        this.init();
    }

    // HTML escape function to prevent XSS
    escapeHtml(text) {
        if (text == null) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    init() {
        this.setupNavigation();
        this.setupEventListeners();
        this.loadInitialData();
    }

    setupNavigation() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const page = e.currentTarget.getAttribute('data-page');
                this.navigateTo(page);
            });
        });
    }

    setupEventListeners() {
        // Run analysis button
        const runBtn = document.getElementById('runAnalysisBtn');
        if (runBtn) {
            runBtn.addEventListener('click', () => this.runAnalysis());
        }

        // IPC event listeners
        if (window.storageAPI) {
            window.storageAPI.onAnalysisStarted(() => {
                this.onAnalysisStarted();
            });

            window.storageAPI.onAnalysisProgress((progress) => {
                this.updateProgress(progress);
            });

            window.storageAPI.onAnalysisComplete((analysis) => {
                this.onAnalysisComplete(analysis);
            });

            window.storageAPI.onAnalysisError((error) => {
                this.onAnalysisError(error);
            });

            window.storageAPI.onOpenSettings(() => {
                this.navigateTo('settings');
            });
        }
    }

    async loadInitialData() {
        try {
            if (window.storageAPI) {
                const analysis = await window.storageAPI.getAnalysis();
                if (analysis) {
                    this.currentAnalysis = analysis;
                    this.updateUI();
                }
            }
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    navigateTo(page) {
        // Update nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('data-page') === page) {
                item.classList.add('active');
            }
        });

        // Update page views
        document.querySelectorAll('.page-view').forEach(view => {
            view.classList.remove('active');
        });
        
        const pageView = document.getElementById(page);
        if (pageView) {
            pageView.classList.add('active');
        }

        this.currentPage = page;
        this.loadPageContent(page);
    }

    async loadPageContent(page) {
        switch (page) {
            case 'dashboard':
                this.loadDashboard();
                break;
            case 'analysis':
                this.loadAnalysisPage();
                break;
            case 'recommendations':
                this.loadRecommendationsPage();
                break;
            case 'storage-plan':
                this.loadStoragePlanPage();
                break;
            case 'caches':
                this.loadCachesPage();
                break;
            case 'dev-environments':
                this.loadDevEnvironmentsPage();
                break;
            case 'applications':
                this.loadApplicationsPage();
                break;
            case 'archive-log':
                await this.loadArchiveLogPage();
                break;
            case 'settings':
                this.loadSettingsPage();
                break;
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            animation: slideIn 0.3s ease;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;

        if (type === 'success') {
            notification.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
        } else if (type === 'error') {
            notification.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
        } else {
            notification.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }

        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    updateProgress(progress) {
        const progressContainer = document.getElementById('analysisProgress');
        const progressFill = document.getElementById('progressFill');
        const progressStatus = document.getElementById('progressStatus');
        const progressTime = document.getElementById('progressTime');

        if (progressFill) {
            progressFill.style.width = progress.percent + '%';
        }
        if (progressStatus) {
            progressStatus.textContent = progress.message || 'Scanning...';
        }
        if (progressTime) {
            const remaining = Math.max(0, 5 - progress.step) * 5;
            progressTime.textContent = remaining > 0 ? `~${remaining}s remaining` : 'Almost done...';
        }
    }

    async runAnalysis() {
        if (this.isAnalyzing) return;

        this.isAnalyzing = true;
        const btn = document.getElementById('runAnalysisBtn');
        const progressContainer = document.getElementById('analysisProgress');

        // Show progress bar
        if (progressContainer) {
            progressContainer.style.display = 'block';
            document.getElementById('progressFill').style.width = '0%';
            document.getElementById('progressStatus').textContent = 'Starting scan...';
            document.getElementById('progressTime').textContent = 'Estimated: ~25s';
        }

        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner"></span><span>Scanning...</span>';
        }

        // Show scanning message in dashboard
        const statsGrid = document.getElementById('statsGrid');
        if (statsGrid) {
            document.getElementById('totalStorage').textContent = '...';
            document.getElementById('reclaimableSpace').textContent = '...';
            document.getElementById('cachesFound').textContent = '...';
            document.getElementById('devBloat').textContent = '...';
        }

        try {
            if (window.storageAPI) {
                const fullSystemScan = document.getElementById('fullSystemScan')?.checked || false;
                const result = await window.storageAPI.runAnalysis({ fullSystemScan });
                if (result.success) {
                    this.currentAnalysis = result.analysis;
                    this.updateUI();
                    const scanTime = result.analysis.scan_duration || '';
                    this.showNotification(`Analysis complete! ${scanTime}`, 'success');
                } else {
                    this.showNotification('Analysis failed: ' + (result.error || 'Unknown error'), 'error');
                }
            } else {
                // Simulate for testing
                await this.simulateAnalysis();
                this.showNotification('Analysis complete!', 'success');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.showNotification('Analysis failed: ' + error.message, 'error');
        } finally {
            this.isAnalyzing = false;
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<span>🚀</span><span>Run Analysis</span>';
            }
            // Hide progress bar after a short delay
            setTimeout(() => {
                if (progressContainer) {
                    progressContainer.style.display = 'none';
                }
            }, 500);
        }
    }

    async simulateAnalysis() {
        // Simulated data for testing
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        this.currentAnalysis = {
            timestamp: new Date().toISOString(),
            summary: {
                total_storage: '156.7 GB',
                reclaimable: '67.3 GB',
                total_files: 12847,
                caches_size: '15.2 GB',
                dev_bloat_size: '32.1 GB'
            },
            recommendations: [
                {
                    priority: 'high',
                    category: 'dev_bloat',
                    title: 'Clean 47 node_modules Folders',
                    description: 'Found 47 node_modules folders totaling 25.3 GB. Most are from old projects.',
                    space_savings: '25.3 GB',
                    risk: 'low',
                    actions: ['Review folders', 'Delete unused', 'Reinstall as needed']
                },
                {
                    priority: 'high',
                    category: 'caches',
                    title: 'Clean Browser and App Caches',
                    description: 'Found 15.2 GB of caches that can be safely deleted.',
                    space_savings: '15.2 GB',
                    risk: 'low',
                    actions: ['Clean Chrome cache', 'Clean Spotify cache', 'Clean system caches']
                },
                {
                    priority: 'medium',
                    category: 'apps',
                    title: 'Review 5 Unused Applications',
                    description: 'Found 5 apps not used in the last 6 months.',
                    space_savings: '8.4 GB',
                    risk: 'medium',
                    actions: ['Review app list', 'Uninstall unused apps']
                }
            ],
            caches: [
                { name: 'Chrome', size: '3.2 GB', safe: true },
                { name: 'Spotify', size: '2.1 GB', safe: true },
                { name: 'Slack', size: '1.8 GB', safe: true },
                { name: 'System Caches', size: '8.1 GB', safe: true }
            ],
            dev_environments: {
                node_modules: { count: 47, size: '25.3 GB' },
                python_venvs: { count: 12, size: '4.8 GB' },
                docker_images: { count: 8, size: '2.0 GB' }
            },
            storage_plan: {
                tier_1_keep_local: { count: 2341, size: '45.2 GB' },
                tier_2_cloud_backup: { count: 1523, size: '28.7 GB' },
                tier_3_archive: { count: 876, size: '15.4 GB' },
                tier_4_safe_delete: { count: 3421, size: '67.4 GB' }
            }
        };
        
        this.updateUI();
    }

    onAnalysisStarted() {
        this.isAnalyzing = true;
        const btn = document.getElementById('runAnalysisBtn');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner"></span><span>Analyzing...</span>';
        }
    }

    onAnalysisProgress(progress) {
        // Could update a progress bar here
        console.log(`Analysis progress: ${progress}%`);
    }

    onAnalysisComplete(analysis) {
        this.isAnalyzing = false;
        this.currentAnalysis = analysis;
        this.updateUI();
        
        const btn = document.getElementById('runAnalysisBtn');
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<span>🚀</span><span>Run Analysis</span>';
        }
    }

    onAnalysisError(error) {
        this.isAnalyzing = false;
        console.error('Analysis error:', error);
        
        const btn = document.getElementById('runAnalysisBtn');
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<span>🚀</span><span>Run Analysis</span>';
        }
    }

    updateUI() {
        this.loadDashboard();
        this.loadPageContent(this.currentPage);
    }

    loadDashboard() {
        if (!this.currentAnalysis) return;

        const summary = this.currentAnalysis.summary || {};
        
        document.getElementById('totalStorage').textContent = summary.total_storage || '--';
        document.getElementById('reclaimableSpace').textContent = summary.reclaimable || '--';
        document.getElementById('cachesFound').textContent = summary.caches_size || '--';
        document.getElementById('devBloat').textContent = summary.dev_bloat_size || '--';

        // Load recent recommendations
        this.loadRecentRecommendations();
    }

    loadRecentRecommendations() {
        const container = document.getElementById('recentRecommendations');
        if (!container) return;

        const recs = this.currentAnalysis?.recommendations || [];
        
        if (recs.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">💡</div>
                    <h3>No Recommendations</h3>
                    <p>Your storage looks good!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = recs.slice(0, 3).map(rec => this.createRecommendationCard(rec)).join('');
    }

    createRecommendationCard(rec) {
        return `
            <div class="recommendation-card ${this.escapeHtml(rec.priority)}">
                <div class="rec-header">
                    <div class="rec-title">${this.escapeHtml(rec.title)}</div>
                    <div class="rec-badge ${this.escapeHtml(rec.priority)}">${this.escapeHtml(rec.priority)}</div>
                </div>
                <div class="rec-description">${this.escapeHtml(rec.description)}</div>
                <div class="rec-meta">
                    <span>💾 ${this.escapeHtml(rec.space_savings)}</span>
                    <span>⚠️ Risk: ${this.escapeHtml(rec.risk)}</span>
                </div>
                <div class="rec-actions">
                    <button class="btn btn-primary btn-sm" onclick="app.executeRecommendation('${this.escapeHtml(rec.category)}')">
                        Execute
                    </button>
                    <button class="btn btn-secondary btn-sm" onclick="app.showDetails('${this.escapeHtml(rec.category)}')">
                        Details
                    </button>
                </div>
            </div>
        `;
    }

    loadAnalysisPage() {
        const container = document.getElementById('analysisContent');
        if (!container || !this.currentAnalysis) return;

        const summary = this.currentAnalysis.summary || {};
        
        container.innerHTML = `
            <div class="content-section">
                <div class="section-header">
                    <h3>Storage Overview</h3>
                </div>
                <div class="stats-grid" style="grid-template-columns: repeat(3, 1fr);">
                    <div class="stat-card">
                        <div class="stat-label">Total Files</div>
                        <div class="stat-value">${summary.total_files?.toLocaleString() || '--'}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Total Storage</div>
                        <div class="stat-value">${summary.total_storage || '--'}</div>
                    </div>
                    <div class="stat-card highlight">
                        <div class="stat-label">Reclaimable</div>
                        <div class="stat-value">${summary.reclaimable || '--'}</div>
                    </div>
                </div>
            </div>
            <div class="content-section">
                <div class="section-header">
                    <h3>Last Analysis</h3>
                </div>
                <p style="color: #666;">
                    ${this.currentAnalysis.timestamp ? new Date(this.currentAnalysis.timestamp).toLocaleString() : 'Unknown'}
                </p>
            </div>
        `;
    }

    loadRecommendationsPage() {
        const container = document.getElementById('recommendationsContent');
        if (!container) return;

        const recs = this.currentAnalysis?.recommendations || [];
        
        if (recs.length === 0) {
            container.innerHTML = `
                <div class="content-section">
                    <div class="empty-state">
                        <div class="empty-state-icon">💡</div>
                        <h3>No Recommendations</h3>
                        <p>Run an analysis to get recommendations</p>
                        <button class="btn btn-primary" onclick="app.runAnalysis()">
                            Run Analysis
                        </button>
                    </div>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="content-section">
                <div class="section-header">
                    <h3>All Recommendations (${recs.length})</h3>
                </div>
                ${recs.map(rec => this.createRecommendationCard(rec)).join('')}
            </div>
        `;
    }

    loadStoragePlanPage() {
        const container = document.getElementById('storagePlanContent');
        if (!container) return;

        const plan = this.currentAnalysis?.storage_plan;
        
        if (!plan) {
            return;
        }

        container.innerHTML = `
            <div class="tier-grid">
                <div class="tier-card tier-1">
                    <div class="tier-title">Tier 1: Keep Local</div>
                    <div class="tier-count">${plan.tier_1_keep_local?.count || 0} files</div>
                    <div class="tier-desc">${plan.tier_1_keep_local?.size || '0 GB'} - Critical, frequently accessed</div>
                </div>
                <div class="tier-card tier-2">
                    <div class="tier-title">Tier 2: Cloud Backup</div>
                    <div class="tier-count">${plan.tier_2_cloud_backup?.count || 0} files</div>
                    <div class="tier-desc">${plan.tier_2_cloud_backup?.size || '0 GB'} - Important, infrequent access</div>
                </div>
                <div class="tier-card tier-3">
                    <div class="tier-title">Tier 3: Archive</div>
                    <div class="tier-count">${plan.tier_3_archive?.count || 0} files</div>
                    <div class="tier-desc">${plan.tier_3_archive?.size || '0 GB'} - Historical, rarely accessed</div>
                </div>
                <div class="tier-card tier-4">
                    <div class="tier-title">Tier 4: Safe Delete</div>
                    <div class="tier-count">${plan.tier_4_safe_delete?.count || 0} files</div>
                    <div class="tier-desc">${plan.tier_4_safe_delete?.size || '0 GB'} - Regenerable, no utility</div>
                </div>
            </div>
            <div class="content-section" style="margin-top: 20px;">
                <div class="section-header">
                    <h3>Execute Storage Plan</h3>
                </div>
                <p style="color: #666; margin-bottom: 15px;">
                    This will move Tier 4 files to trash, archive Tier 3 files, and prepare Tier 2 for cloud backup.
                </p>
                <button class="btn btn-primary" onclick="app.executeStoragePlan()">
                    Execute Plan
                </button>
            </div>
        `;
    }

    loadCachesPage() {
        const container = document.getElementById('cachesContent');
        if (!container) return;

        const caches = this.currentAnalysis?.caches || [];
        
        if (caches.length === 0) {
            return;
        }

        container.innerHTML = `
            <div class="content-section">
                <div class="section-header">
                    <h3>Found Caches (${caches.length})</h3>
                    <button class="btn btn-primary btn-sm" onclick="app.cleanAllCaches()">
                        Clean All
                    </button>
                </div>
                <ul class="item-list">
                    ${caches.map(cache => `
                        <li>
                            <div class="item-info">
                                <div class="item-icon">🗑️</div>
                                <div class="item-details">
                                    <h4>${cache.name}</h4>
                                    <p>${cache.safe ? '✅ Safe to delete' : '⚠️ Review before deleting'}</p>
                                </div>
                            </div>
                            <div class="item-size">${cache.size}</div>
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
    }

    loadDevEnvironmentsPage() {
        const container = document.getElementById('devContent');
        if (!container) return;

        const dev = this.currentAnalysis?.dev_environments;
        
        if (!dev) {
            return;
        }

        container.innerHTML = `
            <div class="content-section">
                <div class="section-header">
                    <h3>Development Bloat</h3>
                    <button class="btn btn-primary btn-sm" onclick="app.cleanDevBloat()">
                        Clean All
                    </button>
                </div>
                <ul class="item-list">
                    <li>
                        <div class="item-info">
                            <div class="item-icon">📦</div>
                            <div class="item-details">
                                <h4>node_modules</h4>
                                <p>${dev.node_modules?.count || 0} folders found</p>
                            </div>
                        </div>
                        <div class="item-size">${dev.node_modules?.size || '0 GB'}</div>
                    </li>
                    <li>
                        <div class="item-info">
                            <div class="item-icon">🐍</div>
                            <div class="item-details">
                                <h4>Python Virtual Environments</h4>
                                <p>${dev.python_venvs?.count || 0} venvs found</p>
                            </div>
                        </div>
                        <div class="item-size">${dev.python_venvs?.size || '0 GB'}</div>
                    </li>
                    <li>
                        <div class="item-info">
                            <div class="item-icon">🐳</div>
                            <div class="item-details">
                                <h4>Docker Images</h4>
                                <p>${dev.docker_images?.count || 0} images found</p>
                            </div>
                        </div>
                        <div class="item-size">${dev.docker_images?.size || '0 GB'}</div>
                    </li>
                </ul>
            </div>
        `;
    }

    loadApplicationsPage() {
        const container = document.getElementById('appsContent');
        if (!container) return;

        // Placeholder - would show actual apps from analysis
        container.innerHTML = `
            <div class="content-section">
                <div class="section-header">
                    <h3>Installed Applications</h3>
                </div>
                <p style="color: #666;">Application analysis coming soon...</p>
            </div>
        `;
    }

    async loadArchiveLogPage() {
        const container = document.getElementById('archiveLogContent');
        if (!container) return;

        try {
            let log = [];
            if (window.storageAPI) {
                log = await window.storageAPI.getArchiveLog();
            }

            if (!log || log.length === 0) {
                container.innerHTML = `
                    <div class="content-section">
                        <div class="empty-state">
                            <div class="empty-state-icon">📋</div>
                            <h3>No Actions Yet</h3>
                            <p>Actions will be logged here when you execute recommendations</p>
                        </div>
                    </div>
                `;
                return;
            }

            container.innerHTML = `
                <div class="content-section">
                    <div class="section-header">
                        <h3>Action History (${log.length})</h3>
                    </div>
                    <ul class="item-list">
                        ${log.map(entry => `
                            <li>
                                <div class="item-info">
                                    <div class="item-icon">${entry.success ? '✅' : '❌'}</div>
                                    <div class="item-details">
                                        <h4>${entry.action}</h4>
                                        <p>${new Date(entry.timestamp).toLocaleString()}</p>
                                    </div>
                                </div>
                                <div class="item-size">${entry.space_freed || '--'}</div>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            `;
        } catch (error) {
            console.error('Error loading archive log:', error);
        }
    }

    loadSettingsPage() {
        // Settings already in HTML, just ensure checkboxes are set
    }

    async executeRecommendation(category) {
        if (!confirm(`Execute ${category} recommendation?`)) return;

        try {
            if (window.storageAPI) {
                const result = await window.storageAPI.executeAction(category, {});
                this.showNotification(result.message || 'Action completed!', 'success');
                await this.runAnalysis();
            } else {
                this.showNotification(`Would execute: ${category}`, 'info');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        }
    }

    async executeQuickAction(action) {
        if (!confirm(`Execute ${action}?`)) return;

        try {
            if (window.storageAPI) {
                const result = await window.storageAPI.executeAction(action, {});
                this.showNotification(result.message || 'Action completed!', 'success');
                await this.runAnalysis();
            } else {
                this.showNotification(`Would execute: ${action}`, 'info');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        }
    }

    async cleanAllCaches() {
        await this.executeQuickAction('clean_caches');
    }

    async cleanDevBloat() {
        await this.executeQuickAction('remove_dev_bloat');
    }

    async executeStoragePlan() {
        await this.executeQuickAction('storage_plan');
    }

    showDetails(category) {
        // Navigate to appropriate page
        switch (category) {
            case 'caches':
                this.navigateTo('caches');
                break;
            case 'dev_bloat':
                this.navigateTo('dev-environments');
                break;
            case 'apps':
                this.navigateTo('applications');
                break;
            default:
                this.navigateTo('analysis');
        }
    }
}

// Initialize app
const app = new StorageIntelligenceApp();
