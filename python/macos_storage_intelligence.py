#!/usr/bin/env python3
"""
macOS Storage Intelligence System
Complete computer analysis with context-aware recommendations

Features:
- System-wide storage analysis
- macOS-specific cache detection
- Personal utility scoring based on user context
- Intelligent storage optimization plans
- Development environment cleanup
- Application usage analysis
- Multi-tiered storage recommendations
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import time
import pwd

class MacOSStorageIntelligence:
    def __init__(self, user_context=None):
        """
        Initialize with user context for intelligent recommendations
        
        Args:
            user_context: Dict with user's work/research context
        """
        self.user = os.getenv('USER')
        self.home = Path.home()
        self.user_context = user_context or self.load_user_context()
        
        # Storage locations to analyze
        self.critical_paths = {
            'home': self.home,
            'desktop': self.home / 'Desktop',
            'documents': self.home / 'Documents',
            'downloads': self.home / 'Downloads',
            'library': self.home / 'Library',
            'applications': Path('/Applications'),
            'dev_projects': self.home / 'Projects',
        }
        
        # macOS-specific cache locations
        self.cache_locations = [
            self.home / 'Library/Caches',
            self.home / 'Library/Application Support',
            self.home / 'Library/Logs',
            self.home / 'Library/Safari',
            self.home / 'Library/Containers',
            Path('/Library/Caches'),
            Path('/System/Library/Caches'),
        ]
        
        # Development environment locations
        self.dev_locations = {
            'node_modules': [],
            'venv': [],
            'docker': self.home / 'Library/Containers/com.docker.docker',
            'xcode': self.home / 'Library/Developer',
            'homebrew': Path('/usr/local/Cellar'),
            'conda': self.home / '.conda',
        }
        
        self.analysis_results = {}
        
    def load_user_context(self):
        """Load or create user context profile"""
        context_file = self.home / '.storage_intelligence' / 'user_context.json'
        
        if context_file.exists():
            with open(context_file, 'r') as f:
                return json.load(f)
        
        # Default context based on what we know about Matheus
        return {
            'profession': 'physician_researcher',
            'primary_work': ['systematic_reviews', 'meta_analysis', 'ai_development'],
            'programming_languages': ['python', 'r', 'javascript', 'typescript'],
            'research_topics': ['neurosurgery', 'cerebellar_stroke', 'medical_ai'],
            'tools_used': [
                'claude', 'cursor', 'vscode', 'rstudio', 'zotero',
                'notion', 'google_drive', 'mega'
            ],
            'storage_priority': {
                'research_papers': 'critical',
                'data_extractions': 'critical',
                'clinical_documents': 'critical',
                'active_code': 'high',
                'old_code': 'medium',
                'media': 'low',
                'caches': 'disposable'
            }
        }
    
    def format_size(self, bytes_size):
        """Human readable size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"
    
    def get_disk_usage(self):
        """Get overall disk usage"""
        try:
            result = subprocess.run(
                ['df', '-h', '/'],
                capture_output=True,
                text=True
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                return {
                    'total': parts[1],
                    'used': parts[2],
                    'available': parts[3],
                    'percent': parts[4]
                }
        except:
            return None
    
    def analyze_directory(self, path, max_depth=3, current_depth=0):
        """Recursively analyze directory with size and age info"""
        
        if current_depth > max_depth:
            return None
        
        path = Path(path)
        if not path.exists() or path.is_symlink():
            return None
        
        result = {
            'path': str(path),
            'name': path.name,
            'type': 'directory' if path.is_dir() else 'file',
            'size': 0,
            'file_count': 0,
            'subdirs': [],
            'oldest_access': None,
            'newest_access': None,
            'file_types': defaultdict(int)
        }
        
        try:
            if path.is_file():
                stat = path.stat()
                result['size'] = stat.st_size
                result['file_count'] = 1
                result['oldest_access'] = stat.st_atime
                result['newest_access'] = stat.st_atime
                result['file_types'][path.suffix.lower() or 'no_extension'] = 1
                return result
            
            # Analyze directory
            for item in path.iterdir():
                try:
                    if item.is_file():
                        stat = item.stat()
                        result['size'] += stat.st_size
                        result['file_count'] += 1
                        result['file_types'][item.suffix.lower() or 'no_extension'] += 1
                        
                        if result['oldest_access'] is None or stat.st_atime < result['oldest_access']:
                            result['oldest_access'] = stat.st_atime
                        if result['newest_access'] is None or stat.st_atime > result['newest_access']:
                            result['newest_access'] = stat.st_atime
                    
                    elif item.is_dir() and not item.name.startswith('.'):
                        subdir = self.analyze_directory(item, max_depth, current_depth + 1)
                        if subdir:
                            result['subdirs'].append(subdir)
                            result['size'] += subdir['size']
                            result['file_count'] += subdir['file_count']
                            
                            if result['oldest_access'] is None or (subdir['oldest_access'] and subdir['oldest_access'] < result['oldest_access']):
                                result['oldest_access'] = subdir['oldest_access']
                            if result['newest_access'] is None or (subdir['newest_access'] and subdir['newest_access'] > result['newest_access']):
                                result['newest_access'] = subdir['newest_access']
                
                except (PermissionError, OSError):
                    continue
        
        except (PermissionError, OSError):
            return None
        
        return result
    
    def find_caches(self):
        """Find and analyze cache directories"""
        
        print("\n🔍 Scanning for caches...")
        
        caches = []
        total_cache_size = 0
        
        for cache_path in self.cache_locations:
            if not cache_path.exists():
                continue
            
            try:
                for item in cache_path.iterdir():
                    if item.is_dir():
                        analysis = self.analyze_directory(item, max_depth=2)
                        if analysis and analysis['size'] > 1024 * 1024:  # > 1MB
                            cache_info = {
                                'path': str(item),
                                'name': item.name,
                                'size': analysis['size'],
                                'size_formatted': self.format_size(analysis['size']),
                                'app': self.identify_app(item.name),
                                'safe_to_delete': self.is_safe_cache(item),
                                'last_access': analysis['newest_access']
                            }
                            caches.append(cache_info)
                            total_cache_size += analysis['size']
            except (PermissionError, OSError):
                continue
        
        # Sort by size
        caches.sort(key=lambda x: x['size'], reverse=True)
        
        return {
            'caches': caches[:50],  # Top 50
            'total_size': total_cache_size,
            'total_size_formatted': self.format_size(total_cache_size),
            'count': len(caches)
        }
    
    def find_development_bloat(self):
        """Find node_modules, venv, build artifacts, etc."""
        
        print("\n🔍 Scanning for development bloat...")
        
        bloat = {
            'node_modules': [],
            'python_venv': [],
            'build_artifacts': [],
            'docker_images': [],
            'total_size': 0
        }
        
        # Find node_modules
        for root, dirs, files in os.walk(self.home):
            # Skip system directories
            if any(skip in root for skip in ['/Library/', '/.', '/Applications/']):
                continue
            
            if 'node_modules' in dirs:
                nm_path = Path(root) / 'node_modules'
                analysis = self.analyze_directory(nm_path, max_depth=1)
                if analysis:
                    bloat['node_modules'].append({
                        'path': str(nm_path),
                        'project': Path(root).name,
                        'size': analysis['size'],
                        'size_formatted': self.format_size(analysis['size']),
                        'last_access': analysis['newest_access'],
                        'age_days': (time.time() - analysis['newest_access']) / (24 * 3600) if analysis['newest_access'] else None
                    })
                    bloat['total_size'] += analysis['size']
                
                # Don't recurse into node_modules
                dirs.remove('node_modules')
            
            # Find Python virtual environments
            if 'venv' in dirs or '.venv' in dirs or 'env' in dirs:
                for venv_name in ['venv', '.venv', 'env']:
                    if venv_name in dirs:
                        venv_path = Path(root) / venv_name
                        analysis = self.analyze_directory(venv_path, max_depth=1)
                        if analysis and analysis['size'] > 10 * 1024 * 1024:  # > 10MB
                            bloat['python_venv'].append({
                                'path': str(venv_path),
                                'project': Path(root).name,
                                'size': analysis['size'],
                                'size_formatted': self.format_size(analysis['size']),
                                'last_access': analysis['newest_access'],
                                'age_days': (time.time() - analysis['newest_access']) / (24 * 3600) if analysis['newest_access'] else None
                            })
                            bloat['total_size'] += analysis['size']
                        
                        dirs.remove(venv_name)
        
        # Check Docker storage
        docker_path = self.home / 'Library/Containers/com.docker.docker/Data'
        if docker_path.exists():
            analysis = self.analyze_directory(docker_path, max_depth=1)
            if analysis:
                bloat['docker_images'].append({
                    'path': str(docker_path),
                    'size': analysis['size'],
                    'size_formatted': self.format_size(analysis['size'])
                })
                bloat['total_size'] += analysis['size']
        
        bloat['total_size_formatted'] = self.format_size(bloat['total_size'])
        
        return bloat
    
    def analyze_applications(self):
        """Analyze installed applications and their usage"""
        
        print("\n🔍 Analyzing applications...")
        
        apps = []
        
        for app_path in Path('/Applications').iterdir():
            if app_path.suffix == '.app':
                try:
                    # Get app size
                    result = subprocess.run(
                        ['du', '-sk', str(app_path)],
                        capture_output=True,
                        text=True
                    )
                    size_kb = int(result.stdout.split()[0])
                    size_bytes = size_kb * 1024
                    
                    # Get last access time
                    stat = app_path.stat()
                    
                    apps.append({
                        'name': app_path.stem,
                        'path': str(app_path),
                        'size': size_bytes,
                        'size_formatted': self.format_size(size_bytes),
                        'last_accessed': stat.st_atime,
                        'age_days': (time.time() - stat.st_atime) / (24 * 3600)
                    })
                
                except:
                    continue
        
        # Sort by size
        apps.sort(key=lambda x: x['size'], reverse=True)
        
        return apps
    
    def calculate_utility_score(self, item_info):
        """
        Calculate personal utility score (0-100) based on user context
        
        Factors:
        - Recency of access (0-30 points)
        - File type relevance (0-25 points)
        - Project relevance (0-25 points)
        - Size efficiency (0-20 points)
        """
        
        score = 0
        
        # Recency score (0-30)
        if 'last_access' in item_info and item_info['last_access']:
            days_since_access = (time.time() - item_info['last_access']) / (24 * 3600)
            if days_since_access < 7:
                score += 30
            elif days_since_access < 30:
                score += 25
            elif days_since_access < 90:
                score += 20
            elif days_since_access < 180:
                score += 10
            elif days_since_access < 365:
                score += 5
        
        # File type relevance (0-25)
        path = item_info.get('path', '').lower()
        
        # Critical work files
        if any(keyword in path for keyword in ['research', 'paper', 'extraction', 'clinical', 'manuscript']):
            score += 25
        elif any(keyword in path for keyword in ['code', 'project', 'script']):
            score += 20
        elif any(keyword in path for keyword in ['data', 'analysis']):
            score += 20
        elif 'cache' in path:
            score += 0  # Caches have no utility
        
        # Project relevance (0-25)
        if any(keyword in path for keyword in ['cerebellar', 'extract', 'systematic']):
            score += 25  # Main research project
        elif any(keyword in path for keyword in self.user_context.get('research_topics', [])):
            score += 20
        
        # Size efficiency (0-20)
        # Penalize very large files that are old
        if 'size' in item_info:
            size_mb = item_info['size'] / (1024 * 1024)
            if size_mb > 1000:  # > 1GB
                score += 5
            elif size_mb > 100:  # > 100MB
                score += 10
            else:
                score += 20
        
        return min(100, score)
    
    def generate_storage_plan(self, analysis):
        """Generate intelligent multi-tiered storage plan"""
        
        print("\n🎯 Generating intelligent storage plan...")
        
        plan = {
            'tier_1_keep_local': [],      # Critical, frequently accessed
            'tier_2_cloud_backup': [],     # Important, infrequent access
            'tier_3_archive': [],          # Historical, rarely accessed
            'tier_4_safe_delete': [],      # No utility, can be regenerated
            'savings_potential': {}
        }
        
        # Analyze each category
        for category, items in analysis.items():
            if not isinstance(items, list):
                continue
            
            for item in items:
                utility_score = self.calculate_utility_score(item)
                item['utility_score'] = utility_score
                
                # Categorize by utility score
                if utility_score >= 70:
                    plan['tier_1_keep_local'].append(item)
                elif utility_score >= 40:
                    plan['tier_2_cloud_backup'].append(item)
                elif utility_score >= 20:
                    plan['tier_3_archive'].append(item)
                else:
                    plan['tier_4_safe_delete'].append(item)
        
        # Calculate savings
        plan['savings_potential'] = {
            'tier_2_cloud': sum(item.get('size', 0) for item in plan['tier_2_cloud_backup']),
            'tier_3_archive': sum(item.get('size', 0) for item in plan['tier_3_archive']),
            'tier_4_delete': sum(item.get('size', 0) for item in plan['tier_4_safe_delete']),
            'total_reclaimable': sum(
                item.get('size', 0) 
                for tier in [plan['tier_2_cloud_backup'], plan['tier_3_archive'], plan['tier_4_safe_delete']]
                for item in tier
            )
        }
        
        # Format sizes
        for key in plan['savings_potential']:
            plan['savings_potential'][f'{key}_formatted'] = self.format_size(plan['savings_potential'][key])
        
        return plan
    
    def identify_app(self, name):
        """Identify application from cache name"""
        app_mappings = {
            'com.google.chrome': 'Google Chrome',
            'com.apple.safari': 'Safari',
            'com.microsoft': 'Microsoft',
            'com.docker': 'Docker',
            'com.electron': 'Electron Apps',
        }
        
        for key, value in app_mappings.items():
            if key in name.lower():
                return value
        
        return name
    
    def is_safe_cache(self, path):
        """Determine if cache is safe to delete"""
        
        path_str = str(path).lower()
        
        # Always safe
        safe_patterns = [
            'browser', 'chrome', 'safari', 'firefox',
            'temp', 'tmp', 'cache',
            'spotify', 'slack'
        ]
        
        # Be careful with these
        unsafe_patterns = [
            'keychain', 'password', 'credential',
            'certificate', 'license'
        ]
        
        if any(pattern in path_str for pattern in unsafe_patterns):
            return False
        
        if any(pattern in path_str for pattern in safe_patterns):
            return True
        
        return False  # Default to cautious
    
    def run_complete_analysis(self):
        """Run complete system analysis"""
        
        print("="*70)
        print("🤖 macOS STORAGE INTELLIGENCE - COMPLETE SYSTEM ANALYSIS")
        print("="*70)
        print(f"\nUser: {self.user}")
        print(f"Home: {self.home}")
        print(f"Context: {self.user_context['profession']}")
        print("")
        
        # Disk usage
        print("💾 Overall Disk Usage:")
        disk = self.get_disk_usage()
        if disk:
            print(f"   Total: {disk['total']}")
            print(f"   Used: {disk['used']} ({disk['percent']})")
            print(f"   Available: {disk['available']}")
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'user': self.user,
            'disk_usage': disk
        }
        
        # Analyze major directories
        print("\n📁 Analyzing major directories...")
        for name, path in self.critical_paths.items():
            if path.exists():
                print(f"   Analyzing {name}...")
                dir_analysis = self.analyze_directory(path, max_depth=2)
                if dir_analysis:
                    analysis[name] = dir_analysis
        
        # Find caches
        analysis['caches'] = self.find_caches()
        
        # Find development bloat
        analysis['dev_bloat'] = self.find_development_bloat()
        
        # Analyze applications
        analysis['applications'] = self.analyze_applications()
        
        # Generate storage plan
        analysis['storage_plan'] = self.generate_storage_plan(analysis)
        
        # Generate recommendations
        analysis['recommendations'] = self.generate_recommendations(analysis)
        
        return analysis
    
    def generate_recommendations(self, analysis):
        """Generate intelligent recommendations"""
        
        recommendations = []
        
        # Cache cleanup
        if analysis.get('caches', {}).get('total_size', 0) > 1024 * 1024 * 1024:  # > 1GB
            recommendations.append({
                'priority': 'high',
                'category': 'cache_cleanup',
                'title': f'Clean {analysis["caches"]["total_size_formatted"]} of Caches',
                'description': f'Found {analysis["caches"]["count"]} cache directories consuming '
                              f'{analysis["caches"]["total_size_formatted"]}. Most can be safely deleted.',
                'actions': [
                    'Review cache list in dashboard',
                    'Delete browser caches',
                    'Clear Spotify/Slack caches',
                    'Keep essential system caches'
                ],
                'space_savings': analysis["caches"]["total_size_formatted"],
                'risk': 'low'
            })
        
        # Development bloat
        if analysis.get('dev_bloat', {}).get('total_size', 0) > 5 * 1024 * 1024 * 1024:  # > 5GB
            recommendations.append({
                'priority': 'high',
                'category': 'dev_cleanup',
                'title': f'Clean {analysis["dev_bloat"]["total_size_formatted"]} of Development Files',
                'description': f'Found {len(analysis["dev_bloat"]["node_modules"])} node_modules and '
                              f'{len(analysis["dev_bloat"]["python_venv"])} Python virtual environments.',
                'actions': [
                    'Delete node_modules from old projects',
                    'Remove unused Python virtual environments',
                    'Clear Docker images',
                    'Reinstall if needed (fast with package managers)'
                ],
                'space_savings': analysis["dev_bloat"]["total_size_formatted"],
                'risk': 'low'
            })
        
        # Large old applications
        old_apps = [app for app in analysis.get('applications', []) 
                   if app['age_days'] > 180 and app['size'] > 500 * 1024 * 1024]
        
        if old_apps:
            total_size = sum(app['size'] for app in old_apps)
            recommendations.append({
                'priority': 'medium',
                'category': 'app_cleanup',
                'title': f'Remove {len(old_apps)} Unused Applications',
                'description': f'Applications not used in 6+ months consuming {self.format_size(total_size)}.',
                'actions': [
                    'Review application list',
                    'Uninstall unused apps',
                    'Keep essential tools',
                    'Reinstall if needed from App Store'
                ],
                'space_savings': self.format_size(total_size),
                'risk': 'medium'
            })
        
        # Storage plan recommendations
        plan = analysis.get('storage_plan', {})
        if plan.get('savings_potential', {}).get('tier_4_delete', 0) > 1024 * 1024 * 1024:
            recommendations.append({
                'priority': 'high',
                'category': 'intelligent_cleanup',
                'title': 'Execute AI Storage Plan',
                'description': f'AI identified {plan["savings_potential"]["tier_4_delete_formatted"]} '
                              f'of files with low personal utility that can be safely removed.',
                'actions': [
                    'Review AI-scored files',
                    'Delete low-utility items',
                    'Move medium-utility to cloud',
                    'Archive historical data'
                ],
                'space_savings': plan["savings_potential"]["total_reclaimable_formatted"],
                'risk': 'low'
            })
        
        return sorted(recommendations, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['priority']])
    
    def save_analysis(self, analysis, output_path=None):
        """Save analysis to file"""
        
        if output_path is None:
            output_path = self.home / '.storage_intelligence' / f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        print(f"\n✅ Analysis saved to: {output_path}")
        
        return output_path

def main():
    """Main execution"""
    
    # Initialize system
    storage_intel = MacOSStorageIntelligence()
    
    # Run analysis
    analysis = storage_intel.run_complete_analysis()
    
    # Print summary
    print("\n" + "="*70)
    print("📊 ANALYSIS SUMMARY")
    print("="*70)
    
    if 'caches' in analysis:
        print(f"\n💾 Caches: {analysis['caches']['total_size_formatted']} "
              f"({analysis['caches']['count']} locations)")
    
    if 'dev_bloat' in analysis:
        print(f"\n🔧 Development Bloat: {analysis['dev_bloat']['total_size_formatted']}")
        print(f"   • node_modules: {len(analysis['dev_bloat']['node_modules'])} projects")
        print(f"   • Python venvs: {len(analysis['dev_bloat']['python_venv'])} environments")
    
    if 'applications' in analysis:
        total_app_size = sum(app['size'] for app in analysis['applications'])
        print(f"\n📱 Applications: {storage_intel.format_size(total_app_size)} "
              f"({len(analysis['applications'])} apps)")
    
    if 'storage_plan' in analysis:
        plan = analysis['storage_plan']
        print(f"\n🎯 Storage Plan:")
        print(f"   • Keep Local: {len(plan['tier_1_keep_local'])} items")
        print(f"   • Cloud Backup: {len(plan['tier_2_cloud_backup'])} items "
              f"({plan['savings_potential']['tier_2_cloud_formatted']})")
        print(f"   • Archive: {len(plan['tier_3_archive'])} items "
              f"({plan['savings_potential']['tier_3_archive_formatted']})")
        print(f"   • Safe Delete: {len(plan['tier_4_safe_delete'])} items "
              f"({plan['savings_potential']['tier_4_delete_formatted']})")
        print(f"\n💰 Total Reclaimable: {plan['savings_potential']['total_reclaimable_formatted']}")
    
    print("\n" + "="*70)
    print("🎯 TOP RECOMMENDATIONS")
    print("="*70)
    
    for i, rec in enumerate(analysis.get('recommendations', [])[:5], 1):
        print(f"\n{i}. [{rec['priority'].upper()}] {rec['title']}")
        print(f"   {rec['description']}")
        print(f"   💾 Space Savings: {rec['space_savings']}")
        print(f"   ⚠️  Risk: {rec['risk']}")
    
    # Save analysis
    output_file = storage_intel.save_analysis(analysis)
    
    print("\n" + "="*70)
    print("✅ COMPLETE! Review full analysis in JSON file.")
    print("="*70 + "\n")
    
    return analysis

if __name__ == "__main__":
    main()
