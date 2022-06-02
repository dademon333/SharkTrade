export default class RestAPIErrors {
    static SERVER_ERROR = 'Internal Server Error';
    static CONNECTION_ERROR = 'Cant connect to server';
    static UNAUTHORIZED = 'Unauthorized';
    static UNKNOWN_ERROR = 'Unknown error';

    static LOGIN_ERROR = 'Invalid email or password';
    static USERNAME_ALREADY_EXISTS = 'Username already exists';
    static EMAIL_ALREADY_EXISTS = 'Email already exists';
    static INVALID_EMAIL = 'Invalid email';
    static INVALID_USERNAME = 'Invalid username';
    static INVALID_PASSWORD = 'Invalid password';

    static TRANSLATIONS = {
        [this.SERVER_ERROR]: 'Произошла ошибка на стороне сервера',
        [this.CONNECTION_ERROR]: 'Ошибка соединения с сервером',
        [this.UNAUTHORIZED]: 'Вы не авторизованы',
        [this.UNKNOWN_ERROR]: 'Произошла неизвестная ошибка',

        [this.LOGIN_ERROR]: 'Неправильный логин или пароль',
        [this.USERNAME_ALREADY_EXISTS]: 'Этот никнейм уже занят',
        [this.EMAIL_ALREADY_EXISTS]: 'Пользователь с такой почтой уже существует',
        [this.INVALID_EMAIL]: 'Это не похоже на email',
        [this.INVALID_USERNAME]: 'Никнейм должен быть от 4 до 30 символов ' +
        'и может состоять только из букв латинского алфавита, ' +
        'цифр и нижних подчеркиваний',
        [this.INVALID_PASSWORD]: 'Пароль должен быть от 8 до 30 символов'
    }
}