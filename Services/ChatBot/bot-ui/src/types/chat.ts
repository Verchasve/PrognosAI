export interface Button {
  title: string;
  payload: string;
}

export interface Message {
  text: string;
  isUser: boolean;
  timestamp: Date;
  buttons?: Button[];
} 