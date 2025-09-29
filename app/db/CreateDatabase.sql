CREATE TABLE usuarios (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) NOT NULL, 
    cpf VARCHAR(11) UNIQUE NOT NULL, 
    email VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE relatorios (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuarios_id UUID NOT NULL,
    conteudo TEXT NOT NULL, 
    data DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (usuarios_id) REFERENCES usuarios(uuid)
)