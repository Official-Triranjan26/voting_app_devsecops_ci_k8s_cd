import globals from "globals";
import pluginJs from "@eslint/js";

export default [
  {
    ignores: ["views/**"],
  },
  pluginJs.configs.recommended,
  {
    languageOptions: {
      // Registers Node.js global variables like require and process
      globals: {
        ...globals.node,
      },
    },
  },
];