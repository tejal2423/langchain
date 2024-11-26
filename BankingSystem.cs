class BankingSystem
{
    private int balance;
    private List<string> transactionHistory = new List<string>();

    public BankingSystem(int initialBalance)
    {
        if (initialBalance < 0)
        {
            Console.WriteLine("Initial balance cannot be negative. Setting balance to 0.");
            balance = 0;
        }
        else
        {
            balance = initialBalance;
        }
    }

    public void Withdraw()
    {
        Console.Write("Enter the amount to withdraw: ");
        if (int.TryParse(Console.ReadLine(), out int amount))
        {
            if (amount <= 0)
            {
                Console.WriteLine("Withdrawal amount must be positive.");
                return;
            }

            if (amount > balance)
            {
                Console.WriteLine("Insufficient balance!");
            }
            else
            {
                balance -= amount;
                Console.WriteLine($"Withdrawal successful. New Balance: {balance}");
                transactionHistory.Add($"Withdrawal: -{amount}, Balance: {balance}, Date: {DateTime.Now}");
            }
        }
        else
        {
            Console.WriteLine("Invalid input! Please enter a valid number.");
        }
    }

    public void Credit()
    {
        Console.Write("Enter the amount to credit: ");
        if (int.TryParse(Console.ReadLine(), out int amount))
        {
            if (amount <= 0)
            {
                Console.WriteLine("Credit amount must be positive.");
                return;
            }

            balance += amount;
            Console.WriteLine($"Credit successful. New Balance: {balance}");
            transactionHistory.Add($"Credit: +{amount}, Balance: {balance}, Date: {DateTime.Now}");
        }
        else
        {
            Console.WriteLine("Invalid input! Please enter a valid number.");
        }
    }

    public void ShowBalance()
    {
        Console.WriteLine($"Current Balance: {balance}");
    }

    public void ShowTransactionHistory()
    {
        Console.WriteLine("Transaction History:");
        if (transactionHistory.Count == 0)
        {
            Console.WriteLine("No transactions found.");
        }
        else
        {
            foreach (var transaction in transactionHistory)
            {
                Console.WriteLine(transaction);
            }
        }
    }

    public static void Main(string[] args)
    {
        Console.Write("Enter the initial balance: ");
        if (!int.TryParse(Console.ReadLine(), out int initialBalance))
        {
            Console.WriteLine("Invalid input! Setting initial balance to 0.");
            initialBalance = 0;
        }

        BankingSystem bank = new BankingSystem(initialBalance);

        
        bank.Credit(); 
        bank.Withdraw(); 
        bank.ShowBalance(); 
        bank.ShowTransactionHistory(); 

        Console.WriteLine("Program has completed the operations. Exiting...");
    }
}
