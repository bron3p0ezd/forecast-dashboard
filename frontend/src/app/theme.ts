import { createTheme } from '@mui/material';
import type { PaletteMode } from '@mui/material';

export const createAppTheme = (mode: PaletteMode) => createTheme({
  palette: {
    mode,
  },
});
