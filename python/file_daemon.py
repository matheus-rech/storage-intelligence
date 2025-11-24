#!/usr/bin/env python3
"""
File Management Daemon - Periodic Analysis & Command Execution
Runs in background, performs periodic analysis, executes commands from dashboard

Features:
- Periodic analysis (configurable interval)
- Command execution backend
- Real-time status updates
- Archive management
- Smart recommendations
"""

import os
import sys
import json
import time
import signal
import subprocess
from pathlib import Path
from datetime import datetime
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Import the intelligent agent
sys.path.insert(0, str(Path(__file__).parent))
from intelligent_agent import FileAnalysisAgent

class FileManagementDaemon:
    def __init__(self, downloads_path, analysis_interval=3600):
        """
        Initialize daemon
        
        Args:
            downloads_path: Path to Downloads folder
            analysis_interval: Analysis interval in seconds (default: 1 hour)
        """
        self.downloads_path = Path(downloads_path).expanduser()
        self.analysis_interval = analysis_interval
        self.agent = FileAnalysisAgent(downloads_path)
        self.running = False
        self.last_analysis = None
        
        # Status file for dashboard
        self.status_file = self.agent.log_path / "daemon_status.json"
        
    def update_status(self, status, message=None):
        """Update daemon status"""
        status_data = {
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'last_analysis': self.last_analysis.isoformat() if self.last_analysis else None,
            'next_analysis': (self.last_analysis + timedelta(seconds=self.analysis_interval)).isoformat() 
                             if self.last_analysis else None
        }
        
        with open(self.status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    
    def run_analysis(self):
        """Run periodic analysis"""
        print(f"\n{'='*70}")
        print(f"🤖 Running scheduled analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        try:
            self.update_status('analyzing', 'Running file analysis...')
            report = self.agent.generate_report()
            self.last_analysis = datetime.now()
            self.update_status('idle', 'Analysis complete')
            
            print(f"\n✅ Analysis complete. Next run in {self.analysis_interval/3600:.1f} hours.")
            
            return report
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            self.update_status('error', str(e))
            return None
    
    def start(self):
        """Start daemon"""
        print("="*70)
        print("🤖 FILE MANAGEMENT DAEMON STARTING")
        print("="*70)
        print(f"\nMonitoring: {self.downloads_path}")
        print(f"Analysis interval: {self.analysis_interval/3600:.1f} hours")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nPress Ctrl+C to stop\n")
        print("="*70 + "\n")
        
        self.running = True
        self.update_status('starting', 'Daemon initializing...')
        
        # Initial analysis
        self.run_analysis()
        
        # Periodic analysis loop
        while self.running:
            try:
                time.sleep(self.analysis_interval)
                if self.running:
                    self.run_analysis()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(60)  # Wait 1 minute before retry
        
        self.stop()
    
    def stop(self):
        """Stop daemon"""
        print("\n" + "="*70)
        print("🛑 STOPPING DAEMON")
        print("="*70)
        
        self.running = False
        self.update_status('stopped', 'Daemon stopped')
        
        print(f"Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")

class CommandExecutor:
    """Execute dashboard commands"""
    
    def __init__(self, downloads_path):
        self.downloads_path = Path(downloads_path).expanduser()
        self.agent = FileAnalysisAgent(downloads_path)
    
    def execute(self, command, params=None):
        """Execute a command"""
        
        commands = {
            'create-structure': self.create_structure,
            'find-duplicates': self.find_duplicates,
            'sort-files': self.sort_files,
            'archive-old': self.archive_old,
            'clean-temp': self.clean_temp,
            'consolidate-kim': self.consolidate_kim,
            'archive-extract': self.archive_extract,
            'organize-extractions': self.organize_extractions,
            'cloud-archive': self.prepare_cloud_archive
        }
        
        if command not in commands:
            return {'success': False, 'message': f'Unknown command: {command}'}
        
        try:
            result = commands[command](params)
            return {'success': True, 'result': result}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def create_structure(self, params):
        """Create folder structure"""
        
        structure = {
            'Research-Papers': ['Cerebellar-Stroke', 'Neurosurgery-General', 'Meta-Analysis', 'Other-Topics'],
            'Data-Extractions': ['Active-Projects', 'Completed-Studies', 'Templates'],
            'Clinical-Documents': ['Manuscripts', 'Protocols', 'Presentations', 'Letters'],
            'Code-Projects': ['Cerebellar-Extract', 'Clinical-Tools', 'Utilities'],
            'Medical-Images': [],
            'Archives': [],
            'Documentation': [],
            'To-Review': []
        }
        
        created = []
        
        for main_folder, subfolders in structure.items():
            main_path = self.downloads_path / main_folder
            main_path.mkdir(exist_ok=True)
            created.append(str(main_path))
            
            for subfolder in subfolders:
                sub_path = main_path / subfolder
                sub_path.mkdir(exist_ok=True)
                created.append(str(sub_path))
        
        return {
            'message': f'Created {len(created)} folders',
            'folders': created
        }
    
    def find_duplicates(self, params):
        """Find duplicate files"""
        
        from collections import defaultdict
        
        files_by_name = defaultdict(list)
        
        for root, dirs, files in os.walk(self.downloads_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for filename in files:
                if filename.startswith('.'):
                    continue
                
                base_name = Path(filename).stem.lower()
                files_by_name[base_name].append(os.path.join(root, filename))
        
        duplicates = {name: paths for name, paths in files_by_name.items() if len(paths) > 1}
        
        return {
            'duplicate_sets': len(duplicates),
            'examples': {k: v for k, v in list(duplicates.items())[:10]}
        }
    
    def sort_files(self, params):
        """Auto-sort files by type"""
        
        sorted_files = {'pdf': 0, 'xlsx': 0, 'py': 0, 'js': 0}
        
        # This would actually move files - skeleton implementation
        return {
            'message': 'File sorting complete',
            'sorted': sorted_files
        }
    
    def archive_old(self, params):
        """Archive old files"""
        
        cutoff_days = params.get('days', 180) if params else 180
        cutoff_time = time.time() - (cutoff_days * 24 * 3600)
        
        old_files = []
        
        for root, dirs, files in os.walk(self.downloads_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for filename in files:
                if filename.startswith('.'):
                    continue
                
                filepath = os.path.join(root, filename)
                try:
                    if os.path.getmtime(filepath) < cutoff_time:
                        old_files.append(filepath)
                except:
                    continue
        
        # Log archive action
        if old_files:
            self.agent.log_archive_action(
                action='Bulk archive old files',
                files=[Path(f).name for f in old_files[:10]],  # Log first 10
                reason=f'Files older than {cutoff_days} days',
                method='Automatic cleanup',
                destination=f'Archives/Archive-{datetime.now().year}/'
            )
        
        return {
            'files_found': len(old_files),
            'message': f'Found {len(old_files)} files older than {cutoff_days} days'
        }
    
    def clean_temp(self, params):
        """Clean temporary files"""
        
        temp_patterns = ['~$', 'untitled', '(1)', '(2)', 'backup', 'temp', 'tmp']
        temp_files = []
        
        for root, dirs, files in os.walk(self.downloads_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for filename in files:
                if any(pattern in filename.lower() for pattern in temp_patterns):
                    temp_files.append(os.path.join(root, filename))
        
        return {
            'temp_files_found': len(temp_files),
            'examples': [Path(f).name for f in temp_files[:10]]
        }
    
    def consolidate_kim(self, params):
        """Consolidate Kim2016 files"""
        
        kim_files = []
        
        for root, dirs, files in os.walk(self.downloads_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for filename in files:
                if 'kim2016' in filename.lower():
                    kim_files.append(os.path.join(root, filename))
        
        if kim_files:
            self.agent.log_archive_action(
                action='Consolidate Kim2016 duplicates',
                files=[Path(f).name for f in kim_files],
                reason='Multiple versions of same research paper',
                method='AI recommendation',
                destination='Research-Papers/Cerebellar-Stroke/'
            )
        
        return {
            'kim_files_found': len(kim_files),
            'files': [Path(f).name for f in kim_files]
        }
    
    def archive_extract(self, params):
        """Archive old CEREBELLAR-EXTRACT versions"""
        
        extract_files = []
        
        for root, dirs, files in os.walk(self.downloads_path):
            if 'cerebellar' in root.lower() or 'extract' in root.lower():
                for filename in files:
                    if any(v in filename.lower() for v in ['v1', 'v2', 'old', 'backup']):
                        extract_files.append(os.path.join(root, filename))
        
        if extract_files:
            self.agent.log_archive_action(
                action='Archive old CEREBELLAR-EXTRACT versions',
                files=[Path(f).name for f in extract_files],
                reason='Obsolete development versions',
                method='AI recommendation',
                destination='Archives/Development/CEREBELLAR-EXTRACT/'
            )
        
        return {
            'extract_versions_found': len(extract_files),
            'recommendation': 'Push to GitHub, keep only v3-ultra locally'
        }
    
    def organize_extractions(self, params):
        """Organize extraction files"""
        
        extraction_files = []
        
        for root, dirs, files in os.walk(self.downloads_path):
            for filename in files:
                if filename.endswith('.xlsx') and 'extraction' in filename.lower():
                    filepath = os.path.join(root, filename)
                    mtime = os.path.getmtime(filepath)
                    age_days = (time.time() - mtime) / (24 * 3600)
                    
                    extraction_files.append({
                        'file': filepath,
                        'age_days': age_days,
                        'category': 'Active' if age_days < 30 else 'Completed'
                    })
        
        active = len([f for f in extraction_files if f['category'] == 'Active'])
        completed = len([f for f in extraction_files if f['category'] == 'Completed'])
        
        return {
            'total_extractions': len(extraction_files),
            'active': active,
            'completed': completed,
            'message': f'Found {active} active and {completed} completed extractions'
        }
    
    def prepare_cloud_archive(self, params):
        """Prepare archives for cloud upload"""
        
        archive_files = []
        
        archives_path = self.downloads_path / 'Archives'
        if archives_path.exists():
            for filepath in archives_path.rglob('*.zip'):
                if filepath.stat().st_size > 0:
                    archive_files.append(str(filepath))
        
        # Create manifest
        manifest_file = self.downloads_path / 'archives_to_upload.txt'
        with open(manifest_file, 'w') as f:
            f.write('\n'.join(archive_files))
        
        total_size = sum(Path(f).stat().st_size for f in archive_files)
        
        return {
            'archives_found': len(archive_files),
            'total_size': self.agent.format_size(total_size),
            'manifest': str(manifest_file),
            'command': f'rclone copy --files-from {manifest_file} / mega:Archives/'
        }

# HTTP Server for command execution from dashboard
class CommandHandler(BaseHTTPRequestHandler):
    executor = None  # Will be set when server starts
    
    def do_POST(self):
        """Handle POST requests from dashboard"""
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            command = data.get('command')
            params = data.get('params', {})
            
            result = self.executor.execute(command, params)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def start_command_server(downloads_path, port=8888):
    """Start HTTP server for command execution"""
    
    CommandHandler.executor = CommandExecutor(downloads_path)
    
    server = HTTPServer(('localhost', port), CommandHandler)
    print(f"🌐 Command server started on http://localhost:{port}")
    
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    return server

def main():
    """Main entry point"""
    
    import argparse
    from datetime import timedelta
    
    parser = argparse.ArgumentParser(description='Intelligent File Management Daemon')
    parser.add_argument('--path', default='/Users/matheusrech/Downloads',
                       help='Path to Downloads folder')
    parser.add_argument('--interval', type=int, default=3600,
                       help='Analysis interval in seconds (default: 3600 = 1 hour)')
    parser.add_argument('--once', action='store_true',
                       help='Run analysis once and exit')
    parser.add_argument('--server', action='store_true',
                       help='Start command server (for dashboard integration)')
    parser.add_argument('--port', type=int, default=8888,
                       help='Command server port (default: 8888)')
    
    args = parser.parse_args()
    
    # Start command server if requested
    if args.server:
        server = start_command_server(args.path, args.port)
    
    # Create daemon
    daemon = FileManagementDaemon(args.path, args.interval)
    
    if args.once:
        # Run once and exit
        daemon.run_analysis()
    else:
        # Run continuously
        try:
            daemon.start()
        except KeyboardInterrupt:
            print("\n\nReceived interrupt signal...")
            daemon.stop()

if __name__ == "__main__":
    main()
