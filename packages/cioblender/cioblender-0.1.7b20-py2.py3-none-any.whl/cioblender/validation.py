
from ciocore.validator import Validator
import logging

logger = logging.getLogger(__name__)

class ValidateScoutFrames(Validator):
    def run(self, _):
        """
        Add a validation warning for a potentially costly scout frame configuration.
        """
        try:
            kwargs = self._submitter
            use_scout_frames = kwargs.get("use_scout_frames")
            chunk_size = kwargs.get("chunk_size")

            if chunk_size > 1 and use_scout_frames:
                msg = "You have chunking set higher than 1."
                msg += " This can cause more scout frames to be rendered than you might expect."
                self.add_warning(msg)

        except Exception as e:
            logger.debug("ValidateScoutFrames: {}".format(e))

class ValidateResolvedChunkSize(Validator):
    def run(self, _):
        """
        Add a validation warning for a potentially costly scout frame configuration.
        """
        try:
            kwargs = self._submitter
            chunk_size = kwargs.get("chunk_size", None)
            resolved_chunk_size = kwargs.get("resolved_chunk_size", None)
            if chunk_size and resolved_chunk_size:
                chunk_size = int(chunk_size)
                resolved_chunk_size = int(resolved_chunk_size)

                if resolved_chunk_size > chunk_size:
                    msg = "The number of frames per task has been automatically increased to maintain " \
                          "a total task count below 800. If you have a time-sensitive deadline and require each frame to be " \
                          "processed on a dedicated instance, you might want to consider dividing the frame range into smaller " \
                          "portions. " \
                          "Alternatively, feel free to reach out to Conductor Customer Support for assistance."
                    self.add_warning(msg)

        except Exception as e:
            logger.debug("ValidateResolvedChunkSize: {}".format(e))

class ValidateGPURendering(Validator):
    def run(self, _):
        """
        Add a validation warning for a using CPU rendering with Eevee.
        """
        try:
            kwargs = self._submitter
            instance_type_family = kwargs.get("instance_type")
            driver_software = kwargs.get("render_software")
            if "eevee" in driver_software.lower() and "cpu" in instance_type_family.lower():
                msg = "CPU rendering is selected."
                msg += " We strongly recommend selecting GPU rendering when using Blender’s render engine, Eevee."
                self.add_warning(msg)
        except Exception as e:
            logger.debug("ValidateGPURendering: {}".format(e))



# Implement more validators here
####################################


def run(kwargs):
    errors, warnings, notices = [], [], []

    er, wn, nt = _run_validators(kwargs)

    errors.extend(er)
    warnings.extend(wn)
    notices.extend(nt)

    return errors, warnings, notices

def _run_validators(kwargs):


    validators = [plugin(kwargs) for plugin in Validator.plugins()]
    logger.debug("Validators: %s", validators)
    for validator in validators:
        validator.run(kwargs)

    errors = list(set.union(*[validator.errors for validator in validators]))
    warnings = list(set.union(*[validator.warnings for validator in validators]))
    notices = list(set.union(*[validator.notices for validator in validators]))
    return errors, warnings, notices


