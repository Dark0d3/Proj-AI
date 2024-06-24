# Prepare training data
TRAIN_DATA = [
    ("""└── Project Folder [
│   ├── Controllers
│   │   ├── HomeController.cs
│   │   └── MvcController.cs
│   ├── Models
│   │   ├── DataModel.cs
│   │   └── User.cs
│   ├── Views
│   │   ├── Shared
│   │   │   └── _Layout.cshtml
│   │   └── Home
│   │       └── Index.cshtml
│   └── Web.config
│
└── Project Folder [
│   ├── Controllers
│   │   ├── HomeController.cs
│   │   └── MvcController.cs
│   ├── Models
│   │   ├── DataModel.cs
│   │   └── User.cs
│   ├── Views
│   │   ├── Shared
│   │   │   └── _Layout.cshtml
│   │   └── Home
│   │       └── Index.cshtml
│   └── Web.config""", {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),
    ("""
    └── Models/
    ├── model1.pth
    ├── model2.pth
    └── ...""", {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),
    ("""│   │   ├── Home.cshtml
│   │   └── Layout.cshtml
│   ├── Controllers/
    """, {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),

    ("""MyWebAPI/
├── Presentation/
│   ├── Controllers/
│   │   └── HomeController.cs
│   ├── Models/
│   │   └── Product.cs
│   ├── Views/
│   │   └── Home/
│   │       └── Index.cshtml
│   └── Startup.cs
├── Application Logic/
│   ├── Services/
│   │   └── ProductService.cs
│   ├── Utilities/
│   │   └── StringUtility.cs
│   └── App.config
├── Data Access/
│   ├── Repositories/
│   │   └── ProductRepository.cs
│   ├── Database/
│   │   └── MyDatabase.db
│   └── ConnectionString.cs
└── Tests/
    └── UnitTests/
        └── ProductServiceTests.cs
    """, {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),

    ("""
│   │    └── database.go // Contains the struct and methods for interacting with the database
│   │
│   ├── Schema/ // Contains the schema for the database tables
│   │    └── user_table.sql // Defines the table structure for the "user" table
│   │
│   ├── Migrations/ // Contains the migration files for creating and modifying the database
│   │    ├── 20210504183619_create_users_table.up.sql // The SQL file for creating the "user" table
│   │    └── 20210504183619_create_users_table.down.sql // The SQL file for dropping the "user" table
│   │
│   ├── Seeds/ // Contains the seed data files for populating the database with initial data
│   │    └── user_seeds.json // JSON file with an array of users to be added to the "user" table
│   │
│   └── README.md // Documentation and information about the project's structure and usage
│
├── ProjAI/ // The main folder for the application
│   ├── cmd/ // Folder for the command-line interface of the application
│   │    └── projai.go // The main file that runs the command-line interface
│   │
│   ├── internal/ // Folder for the core functions and services of the application
│   │    ├── config/ // Folder for configuration files
│   │    │    └── config.go // File containing the configuration options for the application
│   │    │
│   │    ├── db/ // Folder for database interactions
│   │    │    └── db.go // File containing functions for interacting with the database
│   │    │
│   │    ├── handlers/ // Folder for request handling functions and middleware
│   │    │    └── handlers.go // File containing functions for handling HTTP requests and responses
│   │    │
│   │    ├── models/ // Folder for model files defining the structure of data stored in the database
│   │    │    └── user.go // File containing the struct for a "user" object
│   │    │
│   │    ├── repository/ // Folder for database operations and querying
│   │    │    └── repository.go // File containing functions for performing CRUD operations on the database
│   │    │
│   │    └── routes/ // Folder for route definitions
│   │         └── routes.go // File containing the definition of the API routes
│   │
│   ├── main.go // The entry point for the application
│   ├── go.mod // The Go module file
│   └── go.sum // The Go module checksum file
│
├── test/ // Folder for testing files and resources
│    ├── fixtures/ // Folder for test data fixtures
│    │     └── user_fixture.json // JSON file with a sample user object for use in tests
│    │
│    ├── mocks/ // Folder for test doubles and stubs
│    │     └── db_mock.go // Go file defining a mock database interface for testing
│    │
│    └── test_utils.go // File containing helper functions for testing the application
│
├── LICENSE // The license file for the project
└── README.md // The top-level documentation and information about the project
│   │    └── database.go // Contains the struct and methods for interacting with the database
│   │
│   ├── Schema/ // Contains the schema for the database tables
│   │    └── user_table.sql // Defines the table structure for the "user" table
│   │
│   ├── Migrations/ // Contains the migration files for creating and modifying the database
│   │    ├── 20210504183619_create_users_table.up.sql // The SQL file for creating the "user" table
│   │    └── 20210504183619_create_users_table.down.sql // The SQL file for dropping the "user" table
│   │
│   ├── Seeds/ // Contains the seed data files for populating the database with initial data
│   │    └── user_seeds.json // JSON file with an array of users to be added to the "user" table
│   │
│   └── README.md // Documentation and information about the project's structure and usage
│
├── ProjAI/ // The main folder for the application
│   ├── cmd/ // Folder for the command-line interface of the application
│   │    └── projai.go // The main file that runs the command-line interface
│   │
│   ├── internal/ // Folder for the core functions and services of the application
│   │    ├── config/ // Folder for configuration files
│   │    │    └── config.go // File containing the configuration options for the application
│   │    │
│   │    ├── db/ // Folder for database interactions
│   │    │    └── db.go // File containing functions for interacting with the database
│   │    │
│   │    ├── handlers/ // Folder for request handling functions and middleware
│   │    │    └── handlers.go // File containing functions for handling HTTP requests and responses
│   │    │
│   │    ├── models/ // Folder for model files defining the structure of data stored in the database
│   │    │    └── user.go // File containing the struct for a "user" object
│   │    │
│   │    ├── repository/ // Folder for database operations and querying
│   │    │    └── repository.go // File containing functions for performing CRUD operations on the database
│   │    │
│   │    └── routes/ // Folder for route definitions
│   │         └── routes.go // File containing the definition of the API routes
│   │
│   ├── main.go // The entry point for the application
│   ├── go.mod // The Go module file
│   └── go.sum // The Go module checksum file
│
├── test/ // Folder for testing files and resources
│    ├── fixtures/ // Folder for test data fixtures
│    │     └── user_fixture.json // JSON file with a sample user object for use in tests
│    │
│    ├── mocks/ // Folder for test doubles and stubs
│    │     └── db_mock.go // Go file defining a mock database interface for testing
│    │
│    └── test_utils.go // File containing helper functions for testing the application
│
├── LICENSE // The license file for the project
└── README.md // The top-level documentation and information about the project
    """, {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),

    ("""
├── 01_unit_tests/
│   ├── file1.py
│   └── file2.py
├── 02_integration_tests/
│   ├── file3.py
│   └── file4.py
├── 03_functional_tests/
│   ├── file5.py
│   └── file6.py
├── __init__.py
└── test_main.py
    """, {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),


    ("""└── ProductServiceTests.cs
    """, {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),

    ("""Project Folder [
    ├── Controllers
    │   ├── HomeController.cs
    │   └── MvcController.cs
    ├── Models
    │   ├── DataModel.cs
    │   └── User.cs
    ├── Views
    │   ├── Shared
    │   │   └── _Layout.cshtml
    │   └── Home
    │       └── Index.cshtml
    └── Web.config
]
    """, {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),

    ("""/vue-app/
│
├── public/
│   └── index.html      # Main HTML file
│
├── src/
│   ├── assets/         # Static resources like images and fonts
│   ├── components/     # Reusable Vue components
│   │   ├── NavBar.vue
│   │   └── Footer.vue
│   ├── views/          # Vue components that act as pages
│   │   ├── Home.vue
│   │   └── About.vue
│   ├── router/         # Vue router files
│   │   └── index.js
│   ├── store/          # Vuex store files
│   │   └── index.js
│   ├── App.vue         # Main Vue component that wraps others
│   └── main.js         # Entry point for the Vue app
│
├── tests/              # Test files
│   ├── unit/
│   └── e2e/
│
├── .gitignore          # Specifies intentionally untracked files to ignore
├── package.json        # Project metadata and dependencies
└── README.md           # Project overview

    """, {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),

    ("""/react-app/
│
├── public/
│   └── index.html      # Main HTML file
│
├── src/
│   ├── assets/         # Assets like images and global styles
│   ├── components/     # Reusable React components
│   │   ├── NavBar.jsx
│   │   └── Footer.jsx
│   ├── pages/          # Components that act as pages
│   │   ├── Home.jsx
│   │   └── About.jsx
│   ├── utils/          # Utility functions
│   ├── hooks/          # Custom hooks
│   ├── context/        # Context providers
│   ├── App.js          # Main React component
│   ├── index.js        # Entry point for React app, includes routing
│   └── serviceWorker.js# Optional: for progressive web app capabilities
│
├── tests/              # Test files
│   ├── integration/
│   └── unit/
│
├── .gitignore          # Specifies intentionally untracked files to ignore
├── package.json        # Project metadata and dependencies
└── README.md           # Project overview

    """, {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),

     ("""/react-app/
│
├── public/
│   └── index.html      # Main HTML file
│
├── src/
│   ├── assets/         # Assets like images and global styles
│   ├── components/     # Reusable React components
│   │   ├── NavBar.jsx
│   │   └── Footer.jsx
│   ├── pages/          # Components that act as pages
│   │   ├── Home.jsx
│   │   └── About.jsx
│   ├── utils/          # Utility functions


    """, {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),


     ("""
/react-app/
│
├── public/
│   └── index.html      # Main HTML file
│
├── src/
│   ├── assets/         # Assets like images and global styles
│   ├── components/     # Reusable React components
│   │   ├── NavBar.jsx
│   │   └── Footer.jsx


    """, {"cats": {"DIRECTORYSTRUCT": 1.0, "NOTDIRECTORYSTRUCT": 0.0}}),
   
("""C# is a high-level, object-oriented language that is designed to be efficient and easy to use. It supports the use of classes, interfaces, inheritance, polymorphism, and encapsulation, all of which are fundamental concepts in object-oriented programming. C# also has built-in support for functional programming, allowing developers to write code that is more concise and easier to read.

One of the key features of C# is its use of delegates. Delegates are reference types that can be used to represent a method or an event handler. They provide a way to encapsulate a method and make it available for use by other parts of the program. This allows developers to write code that is more flexible and easier to maintain.

Another important feature of C# is its support for lambda expressions. Lambda expressions are small pieces of code that can be used to perform a specific task. They are often used in conjunction with delegates, allowing developers to write code that is more concise and easier to read. """, {"cats": {"DIRECTORYSTRUCT": 0.0, "NOTDIRECTORYSTRUCT": 1.0}}),

(""" Another important feature of C# is its support for lambda expressions. Lambda expressions are small pieces of code that can be used to perform a specific task. They are often used in conjunction with delegates, allowing developers to write code that is more concise and easier to read.

C# also has a strong type system, which helps to prevent common programming errors such as null references. The language provides a range of features for working with data types, including support for generics, interfaces, and inheritance. This makes it easy to write robust and maintainable code that can be used in a variety of situations.

In addition to its core features, C# also has a rich set of libraries and frameworks that make it easy to build a wide range of applications, from simple console programs to large-scale web applications. These include the ASP.NET framework for building web applications, as well as the Entity Framework for working with databases.""", {"cats": {"DIRECTORYSTRUCT": 0.0, "NOTDIRECTORYSTRUCT": 1.0}}),

(""" Overall, C# is a powerful and versatile language that is widely used in the software industry. Its combination of object-oriented programming principles, functional programming features, and strong type system make it a great choice for developers who want to write high-quality code quickly and easily.""", {"cats": {"DIRECTORYSTRUCT": 0.0, "NOTDIRECTORYSTRUCT": 1.0}}),

(""" Vue.js also provides a flexible and powerful templating engine, which allows developers to render their components in a declarative way. This means that instead of writing imperative code that manually adds elements to the DOM, Vue.js automatically manages the update process for you. This makes it easy to write reusable and maintainable code, while also providing good performance.

Another important aspect of Vue.js is its support for two-way data binding. This allows developers to create dynamic and interactive UIs that are tightly integrated with their underlying application logic. By using the v-model directive in your templates, you can easily bind data between your components and your view.

Vue.js also provides a robust ecosystem of tools and resources, including a large community of developers who contribute to its development and maintain its documentation. This makes it easy for developers to find solutions to common problems, as well as to learn from others and improve their skills.""", {"cats": {"DIRECTORYSTRUCT": 0.0, "NOTDIRECTORYSTRUCT": 1.0}}),

("""Vue.js is a progressive and flexible JavaScript framework for building user interfaces and single-page applications. It was designed to be approachable and easy to learn, while also being powerful enough to build complex applications with a clean and modular codebase. Vue.js provides a robust ecosystem of tools and resources, making it an ideal choice for developers of all skill levels.

One of the key features of Vue.js is its component-based architecture. This allows developers to break down their applications into smaller, reusable components that can be easily composed together to form more complex UI elements. This modular approach makes it easy to maintain and update large codebases, as well as to collaborate with other developers on projects. """, {"cats": {"DIRECTORYSTRUCT": 0.0, "NOTDIRECTORYSTRUCT": 1.0}}),

]   