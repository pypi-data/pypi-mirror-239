"""
This file is part of pyemaps backend and its binary dependents.

pyemaps is free software for non-comercial use: you can 
redistribute it and/or modify it under the terms of the GNU General 
Public License as published by the Free Software Foundation, either 
version 3 of the License, or (at your option) any later version.

pyemaps is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyemaps.  If not, see <https://www.gnu.org/licenses/>.

Contact supprort@emlabsoftware.com for any questions and comments.

```

Author:     EMLab Solutions, Inc.
Date:       Oct 20, 2023    
"""
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# root directory for all emaps modules
try:
    from .emaps_sims import dif
except Exception as e:
    print(f'Error loading diffraction simulation modules: {e}')
    raise e

#check other modules existence
try:
    from .emaps_sims import dpgen, csf, powder, bloch, stereo, mxtal

except ImportError as e:
    print(f'Warning: no other simulation modules found in emaps')
    raise e

# try:
#     from .emaps_sims import csf

# except ImportError as e:
#     pass

# try:
#     from .emaps_sims import powder

# except ImportError as e:
#     pass

# try:
#     from .emaps_sims import bloch

# except ImportError as e:
#     pass

# try:
#     from .emaps_sims import stereo

# except ImportError as e:
#     pass


# try:
#     from .emaps_sims import mxtal

# except ImportError as e:
#     print(f'no mxtal module found in emaps')
    
    