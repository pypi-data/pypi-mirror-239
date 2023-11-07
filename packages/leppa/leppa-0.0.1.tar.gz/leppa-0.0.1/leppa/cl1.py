import os

queens = """
    public class EightQueens {
    public static void main(String[] args) {
        int n = 8;
        int[][] board = new int[n][n];
        int row = 0;

        // Place the first Queen and solve the problem
        placeQueens(board, row);

        // Print the final solution
        printBoard(board);
    }

    public static boolean placeQueens(int[][] board, int row) {
        if (row >= board.length) {
            return true; // All Queens have been placed
        }

        int n = board.length;

        for (int col = 0; col < n; col++) {
            if (isSafe(board, row, col)) {
                board[row][col] = 1; // Place Queen

                // Recursively place the remaining Queens
                if (placeQueens(board, row + 1)) {
                    return true; // Successfully placed all Queens
                }

                // If placing the Queen here leads to no solution, backtrack
                board[row][col] = 0;
            }
        }

        return false; // No solution found for this branch
    }

    public static boolean isSafe(int[][] board, int row, int col) {
        int n = board.length;

        // Check the column for any other Queens
        for (int i = 0; i < row; i++) {
            if (board[i][col] == 1) {
                return false;
            }
        }

        // Check upper-left diagonal
        for (int i = row, j = col; i >= 0 && j >= 0; i--, j--) {
            if (board[i][j] == 1) {
                return false;
            }
        }

        // Check upper-right diagonal
        for (int i = row, j = col; i >= 0 && j < n; i--, j++) {
            if (board[i][j] == 1) {
                return false;
            }
        }

        return true; // The placement is safe
    }

    public static void printBoard(int[][] board) {
        for (int[] row : board) {
            for (int cell : row) {
                System.out.print((cell == 1) ? "Q " : ". ");
            }
            System.out.println();
        }
    }
}
"""

zeroone = """
public class zokanp {

    public static void main(String[] args) {
        int[] values = {60, 100, 120};
        int[] weights = {10, 20, 30};
        int maxWeight = 50;

        int maxValue = knapsack(values, weights, maxWeight);
        System.out.println("Maximum value that can be obtained: " + maxValue);
    }

    public static int knapsack(int[] values, int[] weights, int maxWeight) {
        int n = values.length;
        int[][] dp = new int[n + 1][maxWeight + 1];

        for (int i=0; i<=n ;i++){
            for(int w=0; w<= maxWeight; w++){
                if(i==0||w==0){
                    dp[i][w] = 0;
                }
                else if (weights[i-1] <= w){
                    dp[i][w] = Math.max(dp[i-1][w], values[i-1] + dp[i-1][w-weights[i-1]]);
                }
                else {
                    dp[i][w] = dp[i-1][w];
                }
            }
        }

        return dp[n][maxWeight];


    }
}
"""
fractional = """
import java.util.Arrays;
import java.util.Comparator;

public class frackanp {
    public static void main(String[] args) {
        int[] weights = {10, 20, 30};
        int[] values = {60, 100, 120};
        int capacity = 50;

        double maxTotalValue = getMaxTotalValue(weights, values, capacity);
        System.out.println("Maximum total value in the knapsack: " + maxTotalValue);
    }

    public static double getMaxTotalValue(int[] weights, int[] values, int capacity) {
        int n = weights.length;
        Integer[] indices = new Integer[n];
        for (int i = 0; i < n; i++) {
            indices[i] = i;
        }

        Arrays.sort(indices, Comparator.comparingDouble(i -> (double) values[(int) i] / weights[(int) i]).reversed());


        double maxTotalValue = 0.0;
        int remainingCapacity = capacity;

        for (int i : indices) {
            if (remainingCapacity <= 0) {
                break;
            }

            int itemWeight = weights[i];
            int itemValue = values[i];

            if (itemWeight <= remainingCapacity) {
                maxTotalValue += itemValue;
                remainingCapacity -= itemWeight;
            } else {
                double fraction = (double) remainingCapacity / itemWeight;
                maxTotalValue += itemValue * fraction;
                remainingCapacity = 0;
            }
        }

        return maxTotalValue;
    }
}

"""
huffman = """
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Scanner;

public class Huffman {

    public static void printCode(HuffmanNode root, String s){
        if(root.left == null && root.right == null && Character.isLetter(root.c)){
            System.out.println(root.c + ":" + s);
            return;
        }

        printCode(root.left, s + "0");
        printCode(root.right, s + "1");
    }

    public static void main(String[] args) {
        Scanner s = new Scanner(System.in); 

		int n = 6; 
		char[] charArray = { 'a', 'b', 'c', 'd', 'e', 'f' }; 
		int[] charfreq = { 5, 9, 12, 13, 16, 45 };

        PriorityQueue<HuffmanNode> q = new PriorityQueue<>(n, new MyComparator());

        for(int i = 0; i<n; i++){
            HuffmanNode hn = new HuffmanNode();
            hn.c = charArray[i];
            hn.data = charfreq[i];

            hn.left = null;
            hn.right = null;

            q.add(hn);
        }

        HuffmanNode root = null;

        while(q.size() > 1){
            HuffmanNode x = q.peek();
            q.poll();

            HuffmanNode y = q.peek();
            q.poll();

            HuffmanNode f = new HuffmanNode();

            f.data = x.data + y.data;
            f.c = '-';

            f.left = x;
            f.right = y;

            root = f;

            q.add(f);
        }

        printCode(root, "");
    }
}

class HuffmanNode {
    int data;
    char c;

    HuffmanNode left;
    HuffmanNode right;
}

class MyComparator implements Comparator<HuffmanNode> {
    public int compare(HuffmanNode x, HuffmanNode y){
        return x.data - y.data;
    }
}
"""

quicksort = """
public class QuickSort {

        // Function to partion the array on the basis of the pivot value; 

        static int partition(int[] array, int low, int high) {

            int j, temp, i = low + 1;

            Random random = new Random();

            int x = random.nextInt(high - low) + low;

            temp = array[low];

            array[low] = array[x];

            array[x] = temp;

            for (j = low + 1; j <= high; j++) {

                if (array[j] <= array[low] && j != i) {

                    temp = array[j];

                    array[j] = array[i];

                    array[i++] = temp;

                } else if (array[j] <= array[low]) {

                    i++;

                }

            }

            temp = array[i - 1];

            array[i - 1] = array[low];

            array[low] = temp;

            return i - 1;

        }

        // Function to implement quick sort

        static void quickSort(int[] array,int low,int high){

            if(low<high){

                int mid = partition(array,low,high);

                quickSort(array,low,mid-1);
            System.out.println(Arrays.toString(array));

                quickSort(array,mid+1,high);
            System.out.println(Arrays.toString(array));

            }

        }

        // Function to read user input

        public static void main(String[] args) {

            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

            int size;

            System.out.println("Enter the size of the array");

            try {

                size = Integer.parseInt(br.readLine());

            } catch (Exception e) {

                System.out.println("Invalid Input");

                return;

            }

            int[] array = new int[size];

            System.out.println("Enter array elements");

            int i;

            for (i = 0; i < array.length; i++) {

                try {

                    array[i] = Integer.parseInt(br.readLine());

                } catch (Exception e) {

                    System.out.println("An error Occurred");

                }

            }

            System.out.println("The initial array is");

            System.out.println(Arrays.toString(array));

            quickSort(array,0,array.length-1);

            System.out.println("The sorted array is");

            System.out.println(Arrays.toString(array));

        }

    }
"""

gradient = """

current_x = 2
rate = 0.01 # Learning rate
precision = 0.000001  # This tells us when to stop the algorithm
delta_x = 1
max_iterations = 10000 # Maximum number of iterations
iteration_counter = 0

# dy/dx of eqn = 2*(x+3)
def slope(x):
    return 2*(x+3)

def value_y(x):
    return (x+3)**2
y = []
x = []
y.append(value_y(current_x))
x.append(current_x)

while delta_x > precision and iteration_counter < max_iterations:
    previous_x = current_x
    current_x = previous_x - rate * slope(previous_x)
    y.append(value_y(current_x))
    x.append(current_x)
    delta_x = abs(previous_x - current_x)
    print(f"Iteration {iteration_counter+1}")
    iteration_counter += 1
    print(f"X = {current_x}")

print(f"Local Minima occurs at: {current_x}")

plt.scatter(x,y)
plt.xlabel('x-values')
plt.ylabel('y-values')
plt.title('y=(x+3)^2')
plt.show()

"""

bank = """
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
#####################################
df = pd.read_csv("Churn_Modelling.csv")
#####################################
df = df.drop(['RowNumber', 'Surname', 'CustomerId'], axis= 1) #Dropping the unnecessary columns 
#########################################
def visualization(x, y, xlabel):
    plt.figure(figsize=(10,5))
    plt.hist([x, y], color=['red', 'green'], label = ['exit', 'not_exit'])
    plt.xlabel(xlabel,fontsize=20)
    plt.ylabel("No. of customers", fontsize=20)
    plt.legend()
#######################################
df_churn_exited = df[df['Exited']==1]['Tenure']
df_churn_not_exited = df[df['Exited']==0]['Tenure']
##########################################
visualization(df_churn_exited, df_churn_not_exited, "Tenure")
########################################################
df_churn_exited2 = df[df['Exited']==1]['Age']
df_churn_not_exited2 = df[df['Exited']==0]['Age']
#########################################################
visualization(df_churn_exited2, df_churn_not_exited2, "Age")
################################################################
X = df[['CreditScore','Gender','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary']]
states = pd.get_dummies(df['Geography'],drop_first = True)
gender = pd.get_dummies(df['Gender'],drop_first = True)
#################################################################
df = pd.concat([df,gender,states], axis = 1)
####################################################
X = df[['CreditScore','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary','Male','Germany','Spain']]
############################################
y = df['Exited']
############################
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.30)
###################################################
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
#############################################
X_train  = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
#########################################
from keras.models import Sequential 
from keras.layers import Dense 
######################################
classifier = Sequential()
#####################################
classifier.add(Dense(activation = "relu",input_dim = 11,units = 6,kernel_initializer = "uniform")) 
classifier.add(Dense(activation = "relu",units = 6,kernel_initializer = "uniform"))   
####################################
classifier.add(Dense(activation = "sigmoid",units = 1,kernel_initializer = "uniform")) 
#######################################
classifier.compile(optimizer="adam",loss = 'binary_crossentropy',metrics = ['accuracy'])
#################################
classifier.summary()
#############################################
classifier.fit(X_train,y_train,batch_size=10,epochs=50)
########################################
y_pred =classifier.predict(X_test)
y_pred = (y_pred > 0.5) 
#########################################
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
#######################################
cm = confusion_matrix(y_test,y_pred)
######################
accuracy = accuracy_score(y_test,y_pred)
#####################
print(classification_report(y_test,y_pred))

"""
kmeans = """
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#################################
from sklearn.cluster import KMeans, k_means
from sklearn.decomposition import PCA
#######################################
df = pd.read_csv("sales_data_sample.csv")
########################################
df_drop  = ['ADDRESSLINE1', 'ADDRESSLINE2', 'STATUS','POSTALCODE', 'CITY', 'TERRITORY', 'PHONE', 'STATE', 'CONTACTFIRSTNAME', 'CONTACTLASTNAME', 'CUSTOMERNAME', 'ORDERNUMBER']
df = df.drop(df_drop, axis=1)
#########################################
productline = pd.get_dummies(df['PRODUCTLINE']) #Converting the categorical columns. 
Dealsize = pd.get_dummies(df['DEALSIZE'])
##########################################
df = pd.concat([df,productline,Dealsize], axis = 1)
###########################################
df_drop  = ['COUNTRY','PRODUCTLINE','DEALSIZE'] #Dropping Country too as there are alot of countries. 
df = df.drop(df_drop, axis=1)
###########################################
df['PRODUCTCODE'] = pd.Categorical(df['PRODUCTCODE']).codes #Converting the datatype.
#################################################
df.drop('ORDERDATE', axis=1, inplace=True)
###########################################
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(df)
    distortions.append(kmeanModel.inertia_)
############################################
plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()
##############################################
X_train = df.values
####################################
model = KMeans(n_clusters=3,random_state=2) 
model = model.fit(X_train) 
predictions = model.predict(X_train)
###########################################
unique,counts = np.unique(predictions,return_counts=True)
###############################################
counts = counts.reshape(1,3)
######################################
counts_df = pd.DataFrame(counts,columns=['Cluster1','Cluster2','Cluster3'])
########################################
pca = PCA(n_components=2) 
#################################
reduced_X = pd.DataFrame(pca.fit_transform(X_train),columns=['PCA1','PCA2'])
########################################
plt.figure(figsize=(14,10))
plt.scatter(reduced_X['PCA1'],reduced_X['PCA2'])
############################################
reduced_centers = pca.transform(model.cluster_centers_)
#################################################3
plt.figure(figsize=(14,10))
plt.scatter(reduced_X['PCA1'],reduced_X['PCA2'])
plt.scatter(reduced_centers[:,0],reduced_centers[:,1],color='black',marker='x',s=300) 
###############################################
reduced_X['Clusters'] = predictions
##########################################
reduced_X.head()
#####################################
plt.figure(figsize=(14,10))
plt.scatter(reduced_X[reduced_X['Clusters'] == 0].loc[:,'PCA1'],reduced_X[reduced_X['Clusters'] == 0].loc[:,'PCA2'],color='slateblue')
plt.scatter(reduced_X[reduced_X['Clusters'] == 1].loc[:,'PCA1'],reduced_X[reduced_X['Clusters'] == 1].loc[:,'PCA2'],color='springgreen')
plt.scatter(reduced_X[reduced_X['Clusters'] == 2].loc[:,'PCA1'],reduced_X[reduced_X['Clusters'] == 2].loc[:,'PCA2'],color='indigo')
plt.scatter(reduced_centers[:,0],reduced_centers[:,1],color='black',marker='x',s=300)
################################################

"""


uber = """
df = df.drop(['Unnamed: 0', 'key'], axis= 1)
###############################################
df['dropoff_latitude'].fillna(value=df['dropoff_latitude'].mean(),inplace = True)
df['dropoff_longitude'].fillna(value=df['dropoff_longitude'].median(),inplace = True)
#############################################
df.pickup_datetime = pd.to_datetime(df.pickup_datetime, errors='coerce') 
#####################################################
df= df.assign(hour = df.pickup_datetime.dt.hour,
             day= df.pickup_datetime.dt.day,
             month = df.pickup_datetime.dt.month,
             year = df.pickup_datetime.dt.year,
             dayofweek = df.pickup_datetime.dt.dayofweek)
#######################################################
df = df.drop('pickup_datetime',axis=1)
################################################
df.plot(kind = "box",subplots = True,layout = (7,2),figsize=(15,20))
################################################
df = treat_outliers_all(df , df.iloc[: , 0::])
##################################################
df.plot(kind = "box",subplots = True,layout = (7,2),figsize=(15,20))
################################################
import haversine as hs
travel_dist = []
for pos in range(len(df['pickup_longitude'])):
        long1,lati1,long2,lati2 = [df['pickup_longitude'][pos],df['pickup_latitude'][pos],df['dropoff_longitude'][pos],df['dropoff_latitude'][pos]]
        loc1=(lati1,long1)
        loc2=(lati2,long2)
        c = hs.haversine(loc1,loc2)
        travel_dist.append(c)
    
print(travel_dist)
df['dist_travel_km'] = travel_dist
df.head()
#################################################
df= df.loc[(df.dist_travel_km >= 1) | (df.dist_travel_km <= 130)]
print("Remaining observastions in the dataset:", df.shape)
#################################################
incorrect_coordinates = df.loc[(df.pickup_latitude > 90) |(df.pickup_latitude < -90) |
                                   (df.dropoff_latitude > 90) |(df.dropoff_latitude < -90) |
                                   (df.pickup_longitude > 180) |(df.pickup_longitude < -180) |
                                   (df.dropoff_longitude > 90) |(df.dropoff_longitude < -90)
                                    ]

#####################################################
df.drop(incorrect_coordinates, inplace = True, errors = 'ignore')
################################
sns.heatmap(df.isnull()) 
####################################################
corr = df.corr()
################################
fig,axis = plt.subplots(figsize = (10,6))
sns.heatmap(df.corr(),annot = True)
#################################################
x = df[['pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','passenger_count','hour','day','month','year','dayofweek','dist_travel_km']]
#############################################################
y = df['fare_amount']
###########################################
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(x,y,test_size = 0.33)

#############################################################3
from sklearn.linear_model import LinearRegression
regression = LinearRegression()
###################################################
regression.fit(X_train,y_train)
########################################################
regression.intercept_
####################################################
regression.coef_
###############################################
prediction = regression.predict(X_test)
###############################################
from sklearn.metrics import r2_score 
#################################################
r2_score(y_test,prediction)
#############################################
from sklearn.metrics import mean_squared_error
MSE = mean_squared_error(y_test,prediction)
######################################################
RMSE = np.sqrt(MSE)
######################################################
from sklearn.ensemble import RandomForestRegressor
################################################
rf = RandomForestRegressor(n_estimators=100)
###############################################
rf.fit(X_train,y_train)
##################################
y_pred = rf.predict(X_test)
################################################
R2_Random = r2_score(y_test,y_pred)
#########################################
MSE_Random = mean_squared_error(y_test,y_pred)
#############################################
"""

bank_sol = """
pragma solidity ^0.8.0;
contract BankAccount {
    address public owner;
    uint256 public balance;
    constructor() {
        owner = msg.sender;
        balance = 0;
    }
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function deposit(uint256 amount) public onlyOwner {
        require(amount > 0);
        balance += amount;
    }
    function withdraw(uint256 amount) public onlyOwner {
        require(amount > 0);
        require(amount <= balance);
        balance -= amount;
    }
    function getBalance() public view returns (uint256) {
        return balance;
    }
}
"""

student_sol = """
pragma solidity ^0.8.0;
contract StudentData {
    struct Student {
        string name;
        uint256 rollNumber;
        uint256 age;
    }
    Student[] public students;
    constructor() {}

    function addStudent(string memory _name, uint256 _rollNumber, uint256 _age) public {
        Student memory newStudent = Student(_name, _rollNumber, _age);
        students.push(newStudent);
    }

    function getStudentCount() public view returns (uint256) {
        return students.length;
    }

    function getStudent(uint256 index) public view returns (string memory, uint256, uint256) {
        require(index < students.length);
        Student memory student = students[index];
        return (student.name, student.rollNumber, student.age);
    }
}
"""

masterDict = {
    'queens':queens,
    'zeroone': zeroone,
    'fractional': fractional,
    'huffman': huffman,
    'quicksort': quicksort,
    'gradient': gradient,
    'bank': bank,
    'kmeans': kmeans,
    'uber': uber,
    'bank_sol': bank_sol,
    'student_sol': student_sol
}

class Writer:
    def __init__(self, filename):
        self.filename = os.path.join(os.getcwd(), filename)
        self.masterDict = masterDict
        self.questions = list(masterDict.keys())

    def getCode(self, input_string):
        input_string = self.masterDict[input_string]
        with open(self.filename, 'w') as file:
            file.write(input_string)
        print(f'##############################################')

if __name__ == '__main__':
    write = Writer('output.txt')
    # print(write.questions)
    write.getCode('queens')