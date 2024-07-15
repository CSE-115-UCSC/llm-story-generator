import { createTheme } from '@mui/material/styles';

const colors = {
  primary: {
    main: '#9c27b0',
  },
  secondary: {
    main: '#f0f0f0',
  },
  background: {
    default: '#ffffff',
  },
  text: {
    primary: '#000000',
    secondary: '#ffffff',
  },
  messageBubble: {
    user: {
      background: '#f0f0f0',
      text: '#000000',
    },
    bot: {
      background: '#ffffff',
      text: '#000000',
    },
  },
  inputField: {
    background: '#f0f0f0',
    text: '#000000',
  },
  sendButton: {
    background: '#9c27b0',
    text: '#ffffff',
  },
  icons: {
    user: '#808080',
    bot: '#9c27b0',
  },
};

const theme = createTheme({
  palette: {
    primary: colors.primary,
    secondary: colors.secondary,
    background: colors.background,
    text: colors.text,
    custom: {
      inputField: colors.inputField,
      messageBubble: colors.messageBubble,
      icons: colors.icons,
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: colors.background.default,
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          color: colors.text.primary,
        },
      },
    },
    MuiInputBase: {
      styleOverrides: {
        root: {
          backgroundColor: colors.inputField.background,
          color: colors.inputField.text,
          borderRadius: '20px',
          padding: '10px',
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          backgroundColor: colors.sendButton.background,
          color: colors.sendButton.text,
          borderRadius: '50%',
          padding: '10px',
        },
      },
    },
  },
});

export default theme;



