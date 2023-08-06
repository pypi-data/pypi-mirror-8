import xtrabackup.command_executor as command_executor
import xtrabackup.filesystem_utils as filesystem_utils
import xtrabackup.log_manager as log_manager
import xtrabackup.exception as exception
import xtrabackup.timer as timer
import shutil
import logging
from subprocess import CalledProcessError
from sys import stdout


class BackupTool:

    def __init__(self, log_file):
        self.log_manager = log_manager.LogManager()
        self.stop_watch = timer.Timer()
        self.setup_logging(log_file)

    def setup_logging(self, log_file):
        self.logger = logging.getLogger(__name__)
        self.log_manager.attach_file_handler(self.logger, log_file)

    def check_prerequisites(self, repository):
        try:
            filesystem_utils.check_required_binaries(['innobackupex', 'tar'])
            filesystem_utils.check_path_existence(repository)
        except exception.ProgramError:
            self.logger.error('Prerequisites check failed.', exc_info=True)
            raise

    def prepare_workdir(self, path):
        filesystem_utils.mkdir_path(path, 0o755)
        self.workdir = path + '/xtrabackup_tmp'
        self.logger.debug("Temporary workdir: " + self.workdir)
        self.archive_path = path + '/backup.tar.gz'
        self.logger.debug("Temporary archive: " + self.archive_path)

    def exec_backup(self, user, password, thread_count):
        self.stop_watch.start_timer()
        try:
            command_executor.exec_filesystem_backup(
                user,
                password,
                thread_count,
                self.workdir)
        except CalledProcessError as e:
            self.logger.error(
                'An error occured during the backup process.', exc_info=True)
            self.logger.error(
                'Command output: %s', e.output.decode(stdout.encoding))
            self.clean()
            raise
        self.logger.info("Backup time: %s - Duration: %s",
                         self.stop_watch.stop_timer(),
                         self.stop_watch.duration_in_seconds())

    def prepare_backup(self):
        self.stop_watch.start_timer()
        try:
            command_executor.exec_backup_preparation(self.workdir)
        except CalledProcessError as e:
            self.logger.error(
                'An error occured during the preparation process.',
                exc_info=True)
            self.logger.error(
                'Command output: %s', e.output.decode(stdout.encoding))
            self.clean()
            raise
        self.logger.info("Backup preparation time: %s - Duration: %s",
                         self.stop_watch.stop_timer(),
                         self.stop_watch.duration_in_seconds())

    def compress_backup(self):
        self.stop_watch.start_timer()
        try:
            filesystem_utils.create_archive(self.workdir, self.archive_path)
        except CalledProcessError as e:
            self.logger.error(
                'An error occured during the backup compression.',
                exc_info=True)
            self.logger.error('Command output: %s',
                              e.output.decode(stdout.encoding))
            self.clean()
            raise
        self.logger.info("Backup compression time: %s - Duration: %s",
                         self.stop_watch.stop_timer(),
                         self.stop_watch.duration_in_seconds())

    def transfer_backup(self, repository):
        self.stop_watch.start_timer()
        try:
            backup_repository = filesystem_utils.create_sub_repository(
                repository)
            final_archive_path = filesystem_utils.prepare_archive_path(
                backup_repository)
            self.logger.debug("Archive path: " + final_archive_path)
            shutil.move(self.archive_path, final_archive_path)
        except Exception:
            self.logger.error(
                'An error occured during the backup compression.',
                exc_info=True)
            self.clean()
            raise
        self.logger.info("Archive copy time: %s - Duration: %s",
                         self.stop_watch.stop_timer(),
                         self.stop_watch.duration_in_seconds())

    def clean(self):
        shutil.rmtree(self.workdir)
