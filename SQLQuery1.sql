use CINEMA;

CREATE TABLE Movies (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Title NVARCHAR(100) NOT NULL,
    Image NVARCHAR(255) NOT NULL,
    Synopsis NVARCHAR(MAX) NOT NULL,
    Duration INT NOT NULL,
    Classification NVARCHAR(10) NOT NULL,
    Genre NVARCHAR(100) NOT NULL,
    Languaje NVARCHAR(100) NOT NULL
);

CREATE TABLE Seats (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Room NVARCHAR(10) NOT NULL,
    Row NVARCHAR(1) NOT NULL,
    Number INT NOT NULL,
    Available BIT NOT NULL
);

CREATE TABLE Tickets (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Type NVARCHAR(10) NOT NULL,
    Price DECIMAL(5, 2) NOT NULL,
    Promotion NVARCHAR(100)
);

CREATE TABLE Combos (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Description NVARCHAR(100) NOT NULL,
    Price DECIMAL(5, 2) NOT NULL
);

CREATE TABLE Users (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) NOT NULL,
    PurchaseHistory NVARCHAR(MAX)
);

/******************************************************/
INSERT INTO Movies (Title, Image, Synopsis, Duration, Classification, Genre, Languaje)
VALUES 
('Capitán América: Un Nuevo Mundo', 'src/assets/movies/movie1.jpg', 'Cuarta entrega de la franquicia del Capitán América.', 120, '12+ años','Acción', 'Español'),
('Compañera Perfecta', 'src/assets/movies/movie2.jpg', '"Hola. ¿Cansado de pasar? ¿Cansado de que te ignoren? ¿Sientes que te falta una parte de ti? FindYourCompanion.com te garantiza encontrar un Compañero hecho para ti"', 97, '15+ años','Thriller', 'Inglés'),
('Implacable', 'src/assets/movies/movie3.jpg', 'Thug, un exboxeador y sicario de Boston, empieza a perder la memoria al descubrir que su jefe trafica mujeres, decide liberarlas mientras intenta reconectar con su familia.', 112, '12+ años','Acción', 'Español'),
('Las Aventuras de Dog Man', 'src/assets/movies/movie4.jpg', 'Cuando un fiel perro policía y su dueño humano, también oficial de policía, resultan heridos juntos en el trabajo, una cirugía disparatada pero salvadora los une y nace Dog Man. Dog Man está comprometido a proteger y servir. y también a traer objetos, sentarse y dar vueltas. Mientras Dog Man acepta su nueva identidad y se esfuerza por impresionar a su jefe, debe detener los malignos planes del supervillano felino Petey el Gato.', 95, 'Todos','Animación', 'Todos'),
('Médium', 'src/assets/movies/movie5.jpg', 'Cuando Dani (Carolyn Bracken) es brutalmente asesinada en la remota casa de campo que ella y su marido Ted (Gwilym Lee) están renovando, todo el mundo sospecha de un paciente del hospital psiquiátrico local donde Ted trabaja como médico. Pero poco después del trágico asesinato, el sospechoso aparece muerto.', 98, '15+ años','Terror', 'Inglés'),
('One Direction Alcanzando las Estrellas', 'src/assets/movies/movie6.jpg', 'One Direction es sin duda una de las boy band más icónicas de las últimas décadas. Este documental en dos partes revisa el meteórico ascenso de cada uno de sus integrantes a la fama, así como los momentos más determinantes de su historia. Incluye imágenes nunca antes vistas de su gira mundial del 2013, y una serie de detalles sobre sus vidas personales y sus motivaciones para transitar el camino de la fama. Las dos partes se presentan como un solo evento único, y por primera vez en las pantallas grandes de toda Latinoamérica.', 135, '12+ años','Documental', 'Todos'),
('Un Completo Desconocido', 'src/assets/movies/movie7.jpg', 'Ambientada en la vibrante escena musical neoyorquina de principios de los 60´ en pleno revuelo cultural, un enigmático joven de 19 años de Minnesota llega al West Village con su guitarra y un talento revolucionario, destinado a cambiar el curso de la música estadounidense. Mientras entabla sus relaciones más íntimas durante su ascenso a la fama, se siente insatisfecho con el movimiento folk y, negándose a ser encasillado, toma una decisión controversial que resuena culturalmente en todo el mundo.', 141, 'Todos','Documental', 'Todos'),
('Amenaza en el Aire', 'src/assets/movies/movie8.jpg', 'Un oficial que transporta a un fugitivo a través de los páramos de Alaska en una avioneta se ve atrapado cuando sospecha que su piloto no es quien dice ser.', 91, '12+ años','Acción', 'Inglés'),
('Dragon Ball Daima', 'src/assets/movies/movie9.jpg', 'VERSION DOBLADA EPISODIOS 1, 2 y 3 SOLO EN CINES. Goku y compañía vivían una vida tranquila cuando de repente se hicieron pequeños debido a una conspiración. Cuando descubren que la razón de esto puede estar en un mundo conocido como el "Reino Demoniaco", un misterioso joven Majin llamado Glorio aparece ante ellos.', 75, 'Todos','Animación', 'Todos'),
('Hombre Lobo', 'src/assets/movies/movie10.jpg', 'Blake hereda la remota casa donde creció en una zona rural de Oregón tras la desaparición de su propio padre, dado por muerto. Todo se tuerce cuando, de camino a la granja y en plena noche, la familia sufre el brutal ataque de un animal al que no consiguen ver y, en un intento desesperado por huir, se atrincheran dentro de la casa mientras la criatura merodea por la zona.', 102, '12+ años','Horror', 'Español'),
('Interestelar 10th', 'src/assets/movies/movie11.jpg', 'La icónica película de ciencia ficción Interestelar dirigida por Christopher Nolan, conmemora su décimo aniversario con un regreso triunfal a la gran pantalla. Al ver que la vida en la Tierra está llegando a su fin, un grupo de exploradores dirigidos por el piloto Cooper y la científica Amelia emprende una misión que puede ser la más importante de la historia de la humanidad: viajar más allá de nuestra galaxia para descubrir algún planeta en otra que pueda garantizar el futuro de la raza humana.', 169, '12+ años','Acción', 'Español'),
('La Tumba de las Luciernagas', 'src/assets/movies/movie12.jpg', 'Segunda Guerra Mundial, Seita y Setsuko son hijos de un oficial de la marina japonesa que viven en Kobe. Un día, durante un bombardeo, no consiguen llegar a tiempo al búnker donde su madre los espera. Cuando después buscan a su madre, la encuentran malherida en la escuela, que ha sido convertida en un hospital de urgencia.', 88, '12+ años','Animado', 'Español'),
('Moana 2', 'src/assets/movies/movie13.jpg', 'Reúne a Moana y Maui tres años después en un nuevo y extenso viaje junto a una tripulación de inusuales marineros. Tras recibir una inesperada llamada de sus ancestros, Moana debe viajar por los lejanos mares de Oceanía y hacia aguas peligrosas, olvidadas durante mucho tiempo, para vivir una aventura sin precedentes.', 100, 'Todos','Animación', 'Todos'),
('Mufasa: El Rey León', 'src/assets/movies/movie14.jpg', 'Una precuela del éxito de Disney de 2019 "El Rey León".', 120, 'Todos','Aventura', 'Español'),
('Operación Panda', 'src/assets/movies/movie15.jpg', 'La superestrella de acción internacional Jackie Chan participa en una operación de rescate de un querido panda de zoológico llamado Hu Hu.', 99, '12+ años','Acción', 'Español'),
('Paddington en Perú', 'src/assets/movies/movie16.jpg', 'Paddington y la familia Brown visitan a la tía Lucy en Perú, pero un misterio los envía a la selva amazónica y a las montañas peruanas.', 106, 'Todos','Comedia', 'Español'),
('Sonic 3', 'src/assets/movies/movie17.jpg', 'Sonic regresa a la gran pantalla con su aventura más emocionante hasta ahora. Sonic, Knuckles y Tails se reúnen para enfrentarse a un poderoso nuevo adversario: Shadow, un misterioso villano con habilidades nunca vistas. Superados en todos los sentidos, el equipo Sonic deberá buscar una alianza inesperada para detener a Shadow y proteger el planeta.', 110, 'Todos','Animación', 'Todos');

INSERT INTO Seats (Room, Row, Number, Available)
VALUES 
('A', 'A', 1, 1),
('A', 'A', 2, 1),
('A', 'A', 3, 1),
('A', 'A', 4, 1),
('A', 'A', 5, 1),
('A', 'A', 6, 1),
('A', 'A', 7, 1),
('A', 'A', 8, 1),
('A', 'A', 9, 1),
('A', 'A', 10, 1),
('A', 'B', 1, 1),
('A', 'B', 2, 1),
('A', 'B', 3, 1),
('A', 'B', 4, 1),
('A', 'B', 5, 1),
('A', 'B', 6, 1),
('A', 'B', 7, 1),
('A', 'B', 8, 1),
('A', 'B', 9, 1),
('A', 'B', 10, 1),
('A', 'C', 1, 1),
('A', 'C', 2, 1),
('A', 'C', 3, 1),
('A', 'C', 4, 1),
('A', 'C', 5, 1),
('A', 'C', 6, 1),
('A', 'C', 7, 1),
('A', 'C', 8, 1),
('A', 'C', 9, 1),
('A', 'C', 10, 1),
('A', 'C', 11, 1),
('A', 'C', 12, 1),
('A', 'C', 13, 1),
('A', 'C', 14, 1),
('A', 'D', 1, 1),
('A', 'D', 2, 1),
('A', 'D', 3, 1),
('A', 'D', 4, 1),
('A', 'D', 5, 1),
('A', 'D', 6, 1),
('A', 'D', 7, 1),
('A', 'D', 8, 1),
('A', 'D', 9, 1),
('A', 'D', 10, 1),
('A', 'D', 11, 1),
('A', 'D', 12, 1),
('A', 'D', 13, 1),
('A', 'D', 14, 1);

INSERT INTO Tickets (Type, Price, Promotion)
VALUES 
('Niño', 5.00, 'None'),
('Adulto', 10.00, 'None'),
('Adulto Mayor', 7.00, 'None');

INSERT INTO Combos (Description, Price)
VALUES 
('Combo 1: Palomitas y soda', 8.00),
('Combo 2: palomitas grandes y soda', 10.00),
('Combo 3: palomitas y soda grande', 10.00),
('Combo 4: palomitas grandes y soda grande', 12.00);

INSERT INTO Users (Name, Email, PurchaseHistory)
VALUES 
('John Doe', 'john@example.com', 'None');
