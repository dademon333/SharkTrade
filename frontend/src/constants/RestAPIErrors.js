export default class RestAPIErrors {
    static SERVER_ERROR = 'Internal Server Error';
    static CONNECTION_ERROR = 'Cant connect to server';
    static UNAUTHORIZED = 'Not authenticated';
    static UNKNOWN_ERROR = 'Unknown error';
    static NOT_ENOUGH_RIGHTS = 'Not enough rights';

    static LOGIN_ERROR = 'Invalid email or password';
    static USERNAME_ALREADY_EXISTS = 'Username already exists';
    static EMAIL_ALREADY_EXISTS = 'Email already exists';
    static INVALID_EMAIL = 'Invalid email';
    static INVALID_USERNAME = 'Invalid username';
    static INVALID_PASSWORD = 'Invalid password';

    static CANT_WITHDRAW_BID = 'Can\'t withdraw bid';
    static BID_ALREADY_WITHDRAWN = 'Bid already withdrawn';
    static BID_NOT_FOUND = 'Bid not found';

    static LOT_NOT_FOUND = 'lot not found';
    static LOT_IS_CANCELLED = 'lot is cancelled';
    static EXISTS_BIGGER_BID = 'Exists bigger bid';
    static NOT_ENOUGH_MONEY = 'Not enough money';
    static CANT_BID_OWN_LOT = 'Can\'t bid on own lot';

    static TRANSLATIONS = {
        [this.SERVER_ERROR]: 'Произошла ошибка на стороне сервера',
        [this.CONNECTION_ERROR]: 'Ошибка соединения с сервером',
        [this.UNAUTHORIZED]: 'Вы не авторизованы',
        [this.UNKNOWN_ERROR]: 'Произошла неизвестная ошибка',
        [this.NOT_ENOUGH_RIGHTS]: 'Недостаточно прав',

        [this.LOGIN_ERROR]: 'Неправильный логин или пароль',
        [this.USERNAME_ALREADY_EXISTS]: 'Этот никнейм уже занят',
        [this.EMAIL_ALREADY_EXISTS]: 'Пользователь с такой почтой уже существует',
        [this.INVALID_EMAIL]: 'Это не похоже на email',
        [this.INVALID_USERNAME]: 'Никнейм должен быть от 4 до 30 символов ' +
        'и может состоять только из букв латинского алфавита, ' +
        'цифр и нижних подчеркиваний',
        [this.INVALID_PASSWORD]: 'Пароль должен быть от 8 до 30 символов',

        [this.CANT_WITHDRAW_BID]: 'Невозможно вернуть эту ставку',
        [this.BID_ALREADY_WITHDRAWN]: 'Вы уже вернули эту ставку',
        [this.BID_NOT_FOUND]: 'Ставка не найдена',

        [this.LOT_NOT_FOUND]: 'Лот не найден',
        [this.LOT_IS_CANCELLED]: 'Этот аукцион уже завершен',
        [this.EXISTS_BIGGER_BID]: 'Есть ставка выше',
        [this.NOT_ENOUGH_MONEY]: 'Недостаточно денег',
        [this.CANT_BID_OWN_LOT]: 'Это ваш лот'
    }
}