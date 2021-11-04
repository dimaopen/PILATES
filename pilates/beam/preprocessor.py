import os
import logging
import gzip
import shutil

logger = logging.getLogger(__name__)


def copy_plans_from_asim(settings, year, replanning_iteration=-1):
    asim_output_data_dir = settings['asim_local_output_folder']
    beam_scenario_folder = os.path.join(
        settings['beam_local_input_folder'],
        settings['region'],
        settings['beam_scenario_folder'])

    def copy_with_compression_asim_file_to_beam(asim_file_name, beam_file_name):
        asim_file_path = os.path.join(asim_output_data_dir, asim_file_name)
        beam_file_path = os.path.join(beam_scenario_folder, beam_file_name)
        logger.info("Copying asim file %s to beam input scenario file %s", asim_file_path, beam_file_path)

        with open(asim_file_path, 'rb') as f_in, gzip.open(
                beam_file_path, 'wb') as f_out:
            f_out.writelines(f_in)

    copy_with_compression_asim_file_to_beam('final_plans.csv', 'plans.csv.gz')
    if replanning_iteration == -1:
        copy_with_compression_asim_file_to_beam('final_households.csv', 'households.csv.gz')
        copy_with_compression_asim_file_to_beam('final_persons.csv', 'persons.csv.gz')

    if settings.get('final_asim_plans_folder', False):
        beam_local_plans = os.path.join(beam_scenario_folder, 'plans.csv.gz')
        replanning_iteration_number = replanning_iteration + 1
        final_plans_name = f"final_plans_{year}_{replanning_iteration_number:02d}.csv.gz"
        final_plans_location = os.path.join(settings['final_asim_plans_folder'], final_plans_name)
        logger.info("Copying asim plans %s to final asim folder %s", beam_local_plans, final_plans_location)
        shutil.copyfile(beam_local_plans, final_plans_location)

    return
