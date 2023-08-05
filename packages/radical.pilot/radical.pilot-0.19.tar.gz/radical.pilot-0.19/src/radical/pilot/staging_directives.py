#from radical.pilot.utils.logger import logger
import os

# The Staging Directives are specified using a dict in the following form:
#   staging_directive = {
#       'source':   None, # radical.pilot.Url() or string
#       'target':   None, # radical.pilot.Url() or string
#       'action':   None, # COPY, LINK, MOVE, TRANSFER
#       'flags':    None, # CREATE_PARENTS
#       'priority': 0     # Control ordering of actions
#   }

#
# Action operators
#
COPY     = 'Copy'     # local cp
LINK     = 'Link'     # local ln -s
MOVE     = 'Move'     # local mv
TRANSFER = 'Transfer' # saga remote transfer TODO: This might just be a special case of copy

#
# Flags
#
CREATE_PARENTS = 'CreateParents'  # Create parent directories while writing file
SKIP_FAILED    = 'SkipFailed'     # Don't stage out files if tasks failed

#
# Defaults
#
DEFAULT_ACTION   = TRANSFER
DEFAULT_PRIORITY = 0
DEFAULT_FLAGS    = [CREATE_PARENTS, SKIP_FAILED]

#-----------------------------------------------------------------------------
#
def expand_staging_directive(staging_directive, logger):
    """Take an abbreviated or compressed staging directive and expand it.

    """

    # Use this to collect the return value
    new_staging_directive = []

    # We loop over the list of staging directives
    for sd in staging_directive:

        if isinstance(sd, str):

            # We detected a string, convert into dict.  The interpretation
            # differs depending of redirection characters being present in the
            # string.
            append = False
            if  '>>'  in sd :
                src, tgt = sd.split ('>>', 2)
                append   = True
            elif '>'  in sd :
                src, tgt = sd.split ('>',  2)
                append   = False
            elif '<<' in sd :
                tgt, src = sd.split ('<<', 2)
                append   = True
            elif '<'  in sd :
                tgt, src = sd.split ('<',  2)
                append   = False
            else :
                src, tgt = sd, os.path.basename(sd)
                append   = False

            if  append :
                logger.warn ("append mode on staging not supported (ignored)")

            new_sd = {'source':   src.strip(),
                      'target':   tgt.strip(),
                      'action':   DEFAULT_ACTION,
                      'flags':    DEFAULT_FLAGS,
                      'priority': DEFAULT_PRIORITY
            }
            logger.debug("Converting string '%s' into dict '%s'" % (sd, new_sd))
            new_staging_directive.append(new_sd)

        elif isinstance(sd, dict):
            # We detected a dict, will have to distinguish between single and multiple entries

            if not 'action' in sd:
                raise Exception("Staging directive dict has no action member!")
            action = sd['action']

            if 'flags' in sd:
                flags = sd['flags']
            else:
                flags = DEFAULT_FLAGS

            if 'priority' in sd:
                priority = sd['priority']
            else:
                priority = DEFAULT_PRIORITY

            if not 'source' in sd:
                raise Exception("Staging directive dict has no source member!")
            source = sd['source']

            if 'target' in sd:
                target = sd['target']
            else:
                target = os.path.basename(source)

            if isinstance(source, str):
                # This is a regular entry, complete and append it
                new_sd = {'source':   source,
                          'target':   target,
                          'action':   action,
                          'flags':    DEFAULT_FLAGS,
                          'priority': DEFAULT_PRIORITY
                }
                new_staging_directive.append(new_sd)
                logger.debug("Completing entry '%s'" % new_sd)

            elif isinstance(source, list):
                # We detected a list of sources, we want to expand that

                # We will break up the list entries in source into an equal length list of dicts
                new_sds = []

                if target:
                    # Target is also specified, make sure it is a list of equal length

                    if not isinstance(target, list):
                        raise Exception("Both source and target are specified, but target is not a list")

                    if len(source) != len(target):
                        raise Exception("Source (%d) and target (%d) are lists of different length" % (len(source), len(target)))

                    # Now that we have established that the list are of equal size we can combine them
                    for src_entry, tgt_entry in zip(source, target):

                        new_sd = {'source':   src_entry,
                                  'target':   tgt_entry,
                                  'action':   action,
                                  'flags':    flags,
                                  'priority': priority
                        }
                        new_sds.append(new_sd)
                else:
                    # Target is not specified, use the source for the target too.

                    # Go over all entries in the list and create an equal length list of dicts.
                    for src_entry in source:

                        new_sd = {'source':   src_entry,
                                  'target':   os.path.basename(src_entry),
                                  'action':   action,
                                  'flags':    flags,
                                  'priority': priority
                        }
                        new_sds.append(new_sd)

                logger.debug("Converting list '%s' into dicts '%s'" % (source, new_sds))

                # Add the content of the local list to global list
                new_staging_directive.extend(new_sds)

        else:
            raise Exception("Unknown type of staging directive: %s" % sd)

    return new_staging_directive
