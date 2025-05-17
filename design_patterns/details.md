- Design Patterns are just templates of how you should write your code
- The are usually are (how you should write your OOP code) kinda of thing.
- There are three aspects (types) that design patterns are focusing on:
    1. **Creation Patterns**: Those desing patterns are just telling you how you should create your objects and how to build them based on different considerations.
        - Factory: Create the subclass object at the runtime.
        - Abstract Factory: When you want to create families of related class (the relation between chairs and furneture)
        - Builder: In this design pattern you use it when you want to have different objects of the same class but with different configurations.
        - Prototype: In this pattern, you simply create one object then you clone it whenever you want to create a new one, then you change the attributes. (we usually use it when the creation is heavy in computational resources).
        - Singleton: This pattern is used when you want the same instance to be shared between all objects. (This is usually used for a shared configuration, db manager, logging service). (but it creates large coupling)
    
    2. **Structural Patterns:** Those design patterns are focusing more on how the different objects should be composed together to achieve a specific target.
        - Adapter: If you have an object that doesn't fit your system template, then you will write a layer to adapt it (Something like you are using sqlalchemy as an ORM and you want to fit the db_manager object in your template of design)
        - Bridge: You usually make multiple layers of abstraction to be easier to expand and interchange then you crete bridges between the application and the abstract (Something like you create a Box class then you create a Person class and Car class from the Box)
        - Composite: You usually use it when you have an item and a set of items and you want to deal with them in the same way (something like a Box and Polygon or File and Folder) and you simply want to have the same interface (ofcourse with different expected outputs)
        - Decorator: You use this pattern to add a new behaviors to the object during the runtime.
        - Facade: Usually used as a high level interface to use other modules to handle complex requests (something like requesting asking a question from a RAG model, where you do embedding, then retrival, then inference, the CoT, then decoding)
        - Flyweight: Usually used when you want to save memory by simply using the same parts in an object if it's not going to be changed.
        - Proxy: Usually used by adding an extra layer of security before using specific functionality of the object.