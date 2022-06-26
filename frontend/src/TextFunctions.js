class TextFunctions {
    static zeroStart(value, amount) {
        return value.toString().padStart(amount, '0')
    }

    static formatNumber(number) {
        let originalNumber = `${number}`;
        if (typeof number == 'string') {
            number = number.replace(/ /g, '');
        }
        if (number === ''
            || isNaN(number)
            || number === 0) return originalNumber;
        number = Math.floor(number);
        return number
            .toLocaleString()
            .replace(/,/g, ' ')
            .replaceAll(String.fromCharCode(160), ' ');
    }

    static reduceNumber(number) {
        if (number < 1000) {
            return number.toString();
        }

        number = number.toString();
        let length = number.length;
        let newNumber;

        if (length % 3 === 0) {
            newNumber = number.substring(0, 3);
            number = number.substring(3);
        } else if (length % 3 === 1) {
            newNumber = number.substring(0, 1);
            number = number.substring(1);
        } else {
            newNumber = number.substring(0, 2);
            number = number.substring(2);
        }

        if (number[1] !== '0') {
            newNumber += '.' + number.substring(0, 2);
        } else if (number[0] !== '0') {
            newNumber += '.' + number.substring(0, 1);
        }

        newNumber += 'к'.repeat(Math.floor(number.length / 3));
        return newNumber;
    }

    static isNatural(number) {
        return number > 0 && Math.floor(number) === +number;
    }

    static getWordCase(amount, cases) {
        const {nominative, genitiveOne, genitiveMuch} = cases;
        amount = parseInt(amount);

        const remainder10 = amount % 10;
        const remainder100 = Math.floor(amount / 10) % 10;

        if (remainder10 === 1 && remainder100 !== 1)
            return nominative;
        else if ([2, 3, 4].includes(remainder10) && remainder100 !== 1)
            return genitiveOne;
        else
            return genitiveMuch;
    }

    static _formatDays = (days) => {
        const cases = {nominative: 'день', genitiveOne: 'дня', genitiveMuch: 'дней'};
        return `${days} ${this.getWordCase(days, cases)}`;
    }

    static _formatHours = (hours) => {
        const cases = {nominative: 'час', genitiveOne: 'часа', genitiveMuch: 'часов'};
        return `${hours} ${this.getWordCase(hours, cases)}`;
    }

    static _formatMinutes = (minutes) => {
        const cases = {nominative: 'минута', genitiveOne: 'минуты', genitiveMuch: 'минут'};
        return `${minutes} ${this.getWordCase(minutes, cases)}`;
    }

    static _formatSeconds = (seconds) => {
        const cases = {nominative: 'секунда', genitiveOne: 'секунды', genitiveMuch: 'секунд'};
        return `${seconds} ${this.getWordCase(seconds, cases)}`;
    }

    static getTimeDiff(end) {
        if (typeof end === 'string') {
            end = Date.parse(end);
        }

        let diff = Math.floor((end - Date.now()) / 1000);
        diff = Math.max(diff, 0);

        const days = Math.floor(diff / 86400);
        const hours = Math.floor((diff - days * 86400) / 3600);
        const minutes = Math.floor((diff % 3600) / 60);
        const seconds = Math.floor(diff % 60);
        return {days, hours, minutes, seconds};
    }

    static getRemainingTime(end) {
        const {days, hours, minutes, seconds} = this.getTimeDiff(end);
        if (days) {
            return this._formatDays(days);
        }
        if (hours) {
            return this._formatHours(hours);
        }
        if (minutes) {
            return this._formatMinutes(seconds);
        }
        return this._formatSeconds(seconds);
    }

    static parseDateTime(value) {
        const [date, time] = value.split('T');
        const [year, month, day] = date.split('-');
        const [hours, minutes, seconds] = time.split(':');
        return {
            year: parseInt(year),
            month: parseInt(month),
            day: parseInt(day),
            hours: parseInt(hours),
            minutes: parseInt(minutes),
            seconds: parseInt(seconds)
        };
    }

    static formatDateTime(date) {
        const parsed = this.parseDateTime(date);

        const year = this.zeroStart(parsed.year, 4);
        const month = this.zeroStart(parsed.month, 2);
        const day = this.zeroStart(parsed.day, 2);
        const hours = this.zeroStart(parsed.hours, 2);
        const minutes = this.zeroStart(parsed.minutes, 2);

        return `${day}.${month}.${year}, ${hours}:${minutes}`
    }
}

export default TextFunctions;