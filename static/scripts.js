function isNumber(n)
{
    return !isNaN(parseFloat(n)) && isFinite(n);
}

function checkDate(data) {
    return data instanceof Date && !isNaN(data);
}

function format_data(data)
{
    var data1 = data.toString();
    var data2 = "";
    var data3 = "";

    for (let i = 0; i < data1.length; i++)
    {
        if (isNumber(data1[i]))
        {
            data2 = data2 + data1[i];
        }
    }

    for (let i = 0; i < data2.length; i++)
    {
        if (i == 2 || i == 4)
        {
            data3 = data3 + "/" + data2[i];
        }
        else
        {
            data3 = data3 + data2[i]
        }
    }
    return data3;
}

function keyPress_OnlyNumbers(key)
{
    var tmp1 = key.toString();
    var tmp2 = "";

    for (let i = 0; i < tmp1.length; i++)
    {
        if (isNumber(tmp1[i]) && tmp1[i] != " ")
        {
            tmp2 = tmp2 + tmp1[i];
        }
    }
    return tmp2;
}

function format_cardnumber(input)
{
    var tmp = keyPress_OnlyNumbers(input).toString();
    var tmp2 = "";

    for (let i = 0; i < tmp.length; i++)
    {
        if (i % 4 == 0 && i > 0)
        {
            tmp2 = tmp2 + " " + tmp[i];
        }
        else
        {
            tmp2 = tmp2 + tmp[i];
        }
    }

    return tmp2;
}

function checkCard(cardnumber)
{
    // VERIFY IF THE CARD NUMBER IS VALID

    var flag = "";
    var card = keyPress_OnlyNumbers(cardnumber).toString();
    let firstdigits = Number(card[0] + card[1]);
    var isvalid = false;

    let digits = card.length;
    let soma1 = 0;
    let soma2 = 0;

    for (let i = card.length - 1; i >= 0; i--) // a loop that will analize each digit of the card
    {
        let digit = Number(card[i]); // returns the current digit
        if ((i + 1) % 2 == 0) //check if the position of the algarism is pair from the right to the left
        {
            let x = digit * 2; // defines the double of the digit to make the first sum
            if (x < 10) //check if "x" is higher than 10. if it is, it will dismember its algarisms
            {
                soma1 = soma1 + x; // add the digit to the first sum
            }
            else
            {
                for (let j = 0; j < 2; j++) //sum the algarisms of the digit higher than 10
                {
                    let digit2 = x % 10;
                    soma1 = soma1 + digit2;
                    x = Math.round(x / 10);
                }
                // ----
            }
        }
        else //if the position of the algarism is odd, it will be added to another sum
        {
            soma2 = soma2 + digit;
        }
    }
    let somaf = soma1 + soma2;
    if (somaf % 10 == 0) // check if the card number is valid
    {
        isvalid = true;
    }
    // END OF THE CHECKING

    // Verify what is the flag of the card

    if (firstdigits >= 40 && firstdigits < 50 && (digits == 13 || digits == 16) && isvalid)
    {
        flag = "VISA";
    }
    else if (firstdigits > 50 && firstdigits < 56 && digits == 16 && isvalid)
    {
        flag = "MASTERCARD";
    }
    else if ((firstdigits == 34 || firstdigits == 37) && digits == 15 && isvalid)
    {
        flag = "AMEX";
    }
    else
    {
        flag = "INVALID";
    }
    return flag;
}
