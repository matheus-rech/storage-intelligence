#!/usr/bin/env python3
"""
Intelligent File Management Agent
Runs periodic analysis and generates AI-powered recommendations

Features:
- Periodic scanning of Downloads folder
- Space analysis with intelligent recommendations
- Archive logging with detailed tracking
- Dynamic decision support
- Context-aware suggestions
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import time

class FileAnalysisAgent:
    def __init__(self, downloads_path, log_path="~/.file_agent"):
        self.downloads_path = Path(downloads_path).expanduser()
        self.log_path = Path(log_path).expanduser()
        self.log_path.mkdir(exist_ok=True)
        
        self.archive_log_file = self.log_path / "archive_log.json"
        self.recommendations_file = self.log_path / "recommendations.json"
        self.analysis_cache = self.log_path / "analysis_cache.json"
        
    def format_size(self, bytes_size):
        """Convert bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"
    
    def analyze_folder_intelligence(self):
        """Comprehensive intelligent analysis"""
        
        print("🤖 AI Agent: Starting intelligent analysis...")
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'folders': {},
            'recommendations': [],
            'space_insights': [],
            'patterns': []
        }
        
        # Scan all directories
        for root, dirs, files in os.walk(self.downloads_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            if not files:
                continue
            
            folder_name = os.path.basename(root)
            folder_stats = {
                'path': root,
                'file_count': len(files),
                'total_size': 0,
                'file_types': defaultdict(int),
                'oldest_file': None,
                'newest_file': None,
                'avg_age_days': 0
            }
            
            file_ages = []
            
            for filename in files:
                if filename.startswith('.'):
                    continue
                
                filepath = os.path.join(root, filename)
                try:
                    stat = os.stat(filepath)
                    size = stat.st_size
                    mtime = stat.st_mtime
                    age_days = (time.time() - mtime) / (24 * 3600)
                    
                    folder_stats['total_size'] += size
                    ext = Path(filename).suffix.lower()
                    folder_stats['file_types'][ext or 'no_ext'] += 1
                    
                    file_ages.append(age_days)
                    
                    if folder_stats['oldest_file'] is None or age_days > folder_stats['oldest_file']:
                        folder_stats['oldest_file'] = age_days
                    if folder_stats['newest_file'] is None or age_days < folder_stats['newest_file']:
                        folder_stats['newest_file'] = age_days
                        
                except Exception as e:
                    continue
            
            if file_ages:
                folder_stats['avg_age_days'] = sum(file_ages) / len(file_ages)
            
            analysis['folders'][folder_name] = folder_stats
        
        # Generate intelligent recommendations
        analysis['recommendations'] = self.generate_intelligent_recommendations(analysis['folders'])
        analysis['space_insights'] = self.generate_space_insights(analysis['folders'])
        analysis['patterns'] = self.detect_patterns(analysis['folders'])
        
        # Save analysis
        with open(self.analysis_cache, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"✅ Analysis complete. Generated {len(analysis['recommendations'])} recommendations.")
        
        return analysis
    
    def generate_intelligent_recommendations(self, folders):
        """Generate AI-powered recommendations based on analysis"""
        
        recommendations = []
        
        for folder_name, stats in folders.items():
            size_mb = stats['total_size'] / (1024 * 1024)
            
            # Large project folders
            if size_mb > 200 and any(ext in stats['file_types'] for ext in ['.py', '.js', '.ts']):
                recommendations.append({
                    'priority': 'high',
                    'type': 'project-optimization',
                    'folder': folder_name,
                    'size': self.format_size(stats['total_size']),
                    'title': f'Archive {folder_name} Development Files',
                    'description': f'This appears to be a development project ({size_mb:.1f} MB). '
                                   f'Code projects are best managed with version control.',
                    'reason': f'Large code project consuming {size_mb:.1f} MB of local storage',
                    'recommendation': 'Push to GitHub, keep only active development files locally',
                    'actions': [
                        'git init && git add . && git commit -m "Archive"',
                        'git remote add origin <your-repo>',
                        'git push -u origin main',
                        'Move old versions to Archives/'
                    ],
                    'space_savings': self.format_size(stats['total_size'] * 0.7)  # Estimate 70% savings
                })
            
            # Old archives
            if size_mb > 100 and '.zip' in stats['file_types'] and stats['avg_age_days'] > 180:
                recommendations.append({
                    'priority': 'medium',
                    'type': 'cloud-migration',
                    'folder': folder_name,
                    'size': self.format_size(stats['total_size']),
                    'title': f'Move {folder_name} Archives to Cloud',
                    'description': f'{stats["file_count"]} archive files ({size_mb:.1f} MB) averaging '
                                   f'{stats["avg_age_days"]:.0f} days old.',
                    'reason': 'Rarely accessed archives consuming significant local space',
                    'recommendation': 'Upload to MEGA/Google Drive, keep only recent archives locally',
                    'actions': [
                        'Create cloud backup',
                        'Verify upload integrity',
                        'Delete local copies >1 year old',
                        'Keep manifest of archived files'
                    ],
                    'space_savings': self.format_size(stats['total_size'] * 0.8)
                })
            
            # Research paper organization
            if size_mb > 100 and '.pdf' in stats['file_types'] and stats['file_types']['.pdf'] > 50:
                recommendations.append({
                    'priority': 'medium',
                    'type': 'research-organization',
                    'folder': folder_name,
                    'size': self.format_size(stats['total_size']),
                    'title': f'Organize {stats["file_types"][".pdf"]} Research Papers',
                    'description': f'Large collection of PDFs ({stats["file_types"][".pdf"]} files). '
                                   f'Topic-based organization would improve accessibility.',
                    'reason': 'Better organization improves research workflow efficiency',
                    'recommendation': 'Create subfolders by research topic or project',
                    'actions': [
                        'Create topic-based subfolders',
                        'Sort papers by research area',
                        'Use citation manager (Zotero) integration',
                        'Archive papers from completed projects'
                    ],
                    'space_savings': 'No space savings, organizational benefit'
                })
            
            # Data extraction optimization
            if '.xlsx' in stats['file_types'] and stats['file_types']['.xlsx'] > 30:
                recommendations.append({
                    'priority': 'low',
                    'type': 'data-organization',
                    'folder': folder_name,
                    'size': self.format_size(stats['total_size']),
                    'title': f'Organize {stats["file_types"][".xlsx"]} Extraction Files',
                    'description': f'{stats["file_types"][".xlsx"]} Excel files detected. '
                                   f'Separate active from completed extractions.',
                    'reason': 'Clear Active/Completed separation improves workflow',
                    'recommendation': 'Auto-organize by modification date (30 days threshold)',
                    'actions': [
                        'Create Active/ and Completed/ subfolders',
                        'Files modified <30 days → Active',
                        'Older files → Completed',
                        'Archive extractions from finished projects'
                    ],
                    'space_savings': 'Organizational improvement'
                })
        
        return sorted(recommendations, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['priority']])
    
    def generate_space_insights(self, folders):
        """Generate intelligent space usage insights"""
        
        insights = []
        
        total_size = sum(stats['total_size'] for stats in folders.values())
        
        # Sort folders by size
        sorted_folders = sorted(folders.items(), key=lambda x: x[1]['total_size'], reverse=True)
        
        for i, (folder_name, stats) in enumerate(sorted_folders[:5]):
            percentage = (stats['total_size'] / total_size * 100) if total_size > 0 else 0
            
            insight = {
                'folder': folder_name,
                'size': self.format_size(stats['total_size']),
                'percentage': f'{percentage:.1f}%',
                'file_count': stats['file_count'],
                'avg_file_size': self.format_size(stats['total_size'] / stats['file_count']) if stats['file_count'] > 0 else '0 B'
            }
            
            # Add context-specific insight
            if '.pdf' in stats['file_types'] and stats['file_types']['.pdf'] > stats['file_count'] * 0.5:
                insight['context'] = 'Research paper collection'
                insight['suggestion'] = 'Consider citation manager for better organization'
            elif '.zip' in stats['file_types']:
                insight['context'] = 'Archive storage'
                insight['suggestion'] = 'Good candidate for cloud backup'
            elif any(ext in stats['file_types'] for ext in ['.py', '.js', '.ts']):
                insight['context'] = 'Development project'
                insight['suggestion'] = 'Use git for version control'
            else:
                insight['context'] = 'Mixed file types'
                insight['suggestion'] = 'Review for organization opportunities'
            
            insights.append(insight)
        
        return insights
    
    def detect_patterns(self, folders):
        """Detect usage patterns and workflow insights"""
        
        patterns = []
        
        # Detect duplicate file patterns
        file_names = defaultdict(list)
        for folder_name, stats in folders.items():
            folder_path = stats['path']
            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    base_name = Path(filename).stem.lower()
                    file_names[base_name].append(filename)
        
        duplicates = {name: files for name, files in file_names.items() if len(files) > 1}
        
        if len(duplicates) > 10:
            patterns.append({
                'type': 'duplicate-names',
                'severity': 'medium',
                'count': len(duplicates),
                'description': f'Found {len(duplicates)} sets of files with similar names',
                'examples': list(duplicates.keys())[:5],
                'impact': 'Potential version confusion, wasted space',
                'action': 'Run duplicate consolidation tool'
            })
        
        # Detect research workflow patterns
        pdf_count = sum(stats['file_types'].get('.pdf', 0) for stats in folders.values())
        xlsx_count = sum(stats['file_types'].get('.xlsx', 0) for stats in folders.values())
        
        if pdf_count > 100 and xlsx_count > 50:
            patterns.append({
                'type': 'research-workflow',
                'severity': 'info',
                'description': 'Active systematic review workflow detected',
                'details': f'{pdf_count} research papers, {xlsx_count} data files',
                'insight': 'High volume of research materials indicates active systematic review work',
                'optimization': 'Consider dedicated research paper management system'
            })
        
        # Detect development patterns
        code_files = sum(
            stats['file_types'].get(ext, 0)
            for stats in folders.values()
            for ext in ['.py', '.js', '.ts', '.jsx', '.html', '.css']
        )
        
        if code_files > 50:
            patterns.append({
                'type': 'development-activity',
                'severity': 'info',
                'description': 'Active software development detected',
                'details': f'{code_files} code files across projects',
                'insight': 'Multiple development projects ongoing',
                'optimization': 'Use git for version control, archive old projects'
            })
        
        return patterns
    
    def log_archive_action(self, action, files, reason, method, destination=None):
        """Log archive actions with detailed tracking"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'files': files if isinstance(files, list) else [files],
            'file_count': len(files) if isinstance(files, list) else 1,
            'reason': reason,
            'method': method,
            'destination': destination,
            'user': os.getenv('USER', 'unknown')
        }
        
        # Load existing log
        if self.archive_log_file.exists():
            with open(self.archive_log_file, 'r') as f:
                archive_log = json.load(f)
        else:
            archive_log = []
        
        # Add new entry
        archive_log.insert(0, log_entry)
        
        # Keep last 1000 entries
        archive_log = archive_log[:1000]
        
        # Save log
        with open(self.archive_log_file, 'w') as f:
            json.dump(archive_log, f, indent=2)
        
        print(f"📝 Logged: {action} - {len(log_entry['files'])} file(s)")
        
        return log_entry
    
    def get_archive_log(self, limit=50):
        """Retrieve archive log entries"""
        
        if not self.archive_log_file.exists():
            return []
        
        with open(self.archive_log_file, 'r') as f:
            log = json.load(f)
        
        return log[:limit]
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        
        analysis = self.analyze_folder_intelligence()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_folders': len(analysis['folders']),
                'total_size': sum(f['total_size'] for f in analysis['folders'].values()),
                'total_files': sum(f['file_count'] for f in analysis['folders'].values()),
                'recommendations_count': len(analysis['recommendations']),
                'high_priority': len([r for r in analysis['recommendations'] if r['priority'] == 'high']),
                'patterns_detected': len(analysis['patterns'])
            },
            'top_folders_by_size': sorted(
                [
                    {
                        'name': name,
                        'size': self.format_size(stats['total_size']),
                        'files': stats['file_count']
                    }
                    for name, stats in analysis['folders'].items()
                ],
                key=lambda x: analysis['folders'][x['name']]['total_size'],
                reverse=True
            )[:10],
            'recommendations': analysis['recommendations'],
            'space_insights': analysis['space_insights'],
            'patterns': analysis['patterns']
        }
        
        # Format summary
        print("\n" + "="*70)
        print("📊 INTELLIGENT FILE ANALYSIS REPORT")
        print("="*70)
        print(f"\n📁 Total Folders: {report['summary']['total_folders']}")
        print(f"📄 Total Files: {report['summary']['total_files']}")
        print(f"💾 Total Size: {self.format_size(report['summary']['total_size'])}")
        print(f"🎯 Recommendations: {report['summary']['recommendations_count']} "
              f"({report['summary']['high_priority']} high priority)")
        print(f"🔍 Patterns Detected: {report['summary']['patterns_detected']}")
        
        print("\n" + "="*70)
        print("🚨 TOP RECOMMENDATIONS")
        print("="*70)
        
        for i, rec in enumerate(report['recommendations'][:5], 1):
            print(f"\n{i}. [{rec['priority'].upper()}] {rec['title']}")
            print(f"   {rec['description']}")
            print(f"   💡 {rec['recommendation']}")
            if rec.get('space_savings') != 'No space savings, organizational benefit':
                print(f"   💾 Potential savings: {rec['space_savings']}")
        
        print("\n" + "="*70)
        print("📊 SPACE INSIGHTS")
        print("="*70)
        
        for insight in report['space_insights'][:5]:
            print(f"\n📁 {insight['folder']}")
            print(f"   Size: {insight['size']} ({insight['percentage']})")
            print(f"   Files: {insight['file_count']} (avg {insight['avg_file_size']})")
            print(f"   Context: {insight['context']}")
            print(f"   💡 {insight['suggestion']}")
        
        if report['patterns']:
            print("\n" + "="*70)
            print("🔍 DETECTED PATTERNS")
            print("="*70)
            
            for pattern in report['patterns']:
                print(f"\n• {pattern['description']}")
                print(f"  Impact: {pattern.get('impact', pattern.get('insight', 'N/A'))}")
        
        print("\n" + "="*70)
        
        # Save report
        report_file = self.log_path / f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Full report saved to: {report_file}")
        
        return report

def main():
    """Main agent function"""
    
    downloads_path = "/Users/matheusrech/Downloads"
    
    print("="*70)
    print("🤖 INTELLIGENT FILE MANAGEMENT AGENT")
    print("="*70)
    print(f"\nMonitoring: {downloads_path}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize agent
    agent = FileAnalysisAgent(downloads_path)
    
    # Generate comprehensive report
    report = agent.generate_report()
    
    # Example: Log an archive action
    # agent.log_archive_action(
    #     action="Archive old versions",
    #     files=["old_file1.py", "old_file2.py"],
    #     reason="Obsolete development versions",
    #     method="AI recommendation",
    #     destination="Archives/2024/Development/"
    # )
    
    print("\n✨ Analysis complete!")
    print(f"📋 View recommendations in: {agent.recommendations_file}")
    print(f"📝 Archive log: {agent.archive_log_file}")
    
    return report

if __name__ == "__main__":
    main()
