export interface User {
  id: string;
  name?: string;
  avatar?: string;

  [key: string]: unknown;
}
