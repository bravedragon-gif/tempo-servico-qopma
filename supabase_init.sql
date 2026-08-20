-- 1. Criar tabela de usuários
create table if not exists app_users (
  username text primary key,
  password text not null,
  name text not null,
  profile text not null default 'usuario'
);

-- Habilitar RLS e criar políticas públicas para acesso anon
alter table app_users enable row level security;
drop policy if exists "Acesso Público Geral" on app_users;
create policy "Acesso Público Geral" on app_users for all using (true) with check (true);

-- 2. Criar tabela de oficiais
create table if not exists officers (
  id integer primary key,
  name text not null,
  rank text not null,
  agregado boolean not null default false,
  entry_date text not null,
  promotion_date text default '',
  ffaa_years integer not null default 0,
  ffaa_months integer not null default 0,
  ffaa_days integer not null default 0,
  civil_years integer not null default 0,
  civil_months integer not null default 0,
  civil_days integer not null default 0
);

-- Habilitar RLS e criar políticas públicas para acesso anon
alter table officers enable row level security;
drop policy if exists "Acesso Público Oficiais" on officers;
create policy "Acesso Público Oficiais" on officers for all using (true) with check (true);

-- Limpar tabela antes de popular
truncate table officers;

-- 3. Inserir Oficiais Iniciais
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (1, 'CARLOS ROBERTO DE ARAÚJO', 'MAJ', false, '01/01/1988', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (2, 'EDSON DE ARAÚJO AGUIAR', 'MAJ', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (3, 'ARNALDO JOSÉ NEVES', 'MAJ', false, '12/08/1996', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (4, 'JULIANA ALVES FERNANDES DE MELO', 'MAJ', true, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (5, 'MAIRA MRAD TEIXEIRA SILVA', 'MAJ', true, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (6, 'RODRIGO CASTRO DE FREITAS', 'MAJ', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (7, 'GILMAR JOSÉ RODRIGUES', 'MAJ', false, '12/08/1996', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (8, 'GILDÉSIO ALVES DE OLIVEIRA', 'MAJ', false, '01/10/1999', '', 0, 0, 0, 2, 4, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (9, 'GUSTAVO CANDEIA COSTA', 'MAJ', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (10, 'JONAS APARECIDO DIAS', 'MAJ', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (11, 'RODRIGO PRETEL PARENTE CORREIA', 'MAJ', true, '01/10/1999', '', 0, 0, 0, 0, 11, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (12, 'JEISSON ANTÔNIO DA SILVA', 'MAJ', true, '15/05/1996', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (13, 'LEONARDO ANTUNES E SILVA', 'MAJ', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (14, 'ADRIANO GOMES DUARTE', 'MAJ', false, '15/05/1996', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (15, 'JOÃO TIELLES DAMASCENO', 'MAJ', true, '15/05/1996', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (16, 'JEAN KARTER SOUZA DE OLIVEIRA', 'MAJ', false, '15/05/1996', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (17, 'ADRIANO ROSA EDUARDO', 'CAP', true, '01/10/1999', '', 0, 0, 0, 1, 11, 15);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (18, 'CIDCLAY COSTA DE ABREU', 'CAP', false, '15/05/1996', '', 0, 0, 0, 1, 0, 8);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (19, 'DAVI GERMANO', 'CAP', false, '01/08/1993', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (20, 'HUADSON FABRÍCIO BESERRA TEIXEIRA', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (21, 'PAULO DE TARSO ARAÚJO NOGUEIRA', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 6, 2);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (22, 'MÁRCIO PEREIRA COIMBRA', 'CAP', true, '01/10/1999', '', 0, 0, 0, 1, 6, 1);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (23, 'RONAN CASTILHO GONÇALVES', 'CAP', false, '01/10/1999', '', 5, 2, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (24, 'DJALMA GOMES MENDES JUNIOR', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (25, 'EDUARDO ALVES DINIZ', 'CAP', true, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (26, 'ELIAS PEREIRA DE OLIVEIRA JUNIOR', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (27, 'WARLLEY LIMA DA SILVA', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (28, 'JOVINIANO DA SILVA MELO', 'CAP', false, '07/03/1995', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (29, 'CLAUBERT NEVES SÁ ABREU', 'CAP', false, '15/05/1996', '', 0, 0, 0, 0, 3, 9);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (30, 'VANDERLEY ALMEIDA BANDEIRA', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (31, 'NÉLITON LÚCIO ALVES', 'CAP', false, '15/05/1995', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (32, 'NILS NILSON CORRÊA PINHEIRO', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (33, 'MAURICIO JUNIOR PERPETUO SALES', 'CAP', false, '07/03/1995', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (34, 'EUCIMAR DIOGENES DE MEDEIROS', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (35, 'FERNANDO DIAS MARTINS', 'CAP', false, '15/05/1995', '', 0, 0, 0, 0, 10, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (36, 'RIVAN PINTO BONIFÁCIO', 'CAP', false, '01/04/1988', '', 1, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (37, 'JOSE WELLINGTON DE OLIVEIRA BARROS JR', 'CAP', true, '01/10/1999', '', 0, 0, 0, 5, 1, 29);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (38, 'FABIO JUNIO OLIVEIRA RAMOS', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (39, 'ARLAN CHARLES DE SOUSA', 'CAP', false, '01/10/1999', '', 2, 2, 17, 0, 11, 29);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (40, 'EDSON PINTO GOMES', 'CAP', false, '01/10/1999', '', 2, 7, 29, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (41, 'GLAUCO SOARES DE ALMEIDA', 'CAP', false, '10/03/1997', '', 2, 1, 1, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (42, 'CLEUTER GODINHO DO NASCIMENTO', 'CAP', false, '15/05/1996', '', 0, 8, 23, 1, 0, 27);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (43, 'WELLINGTON LEITE DE SOUZA', 'CAP', false, '01/10/1999', '', 0, 0, 0, 1, 1, 10);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (44, 'LEURIMAR DE SOUZA DUTRA', 'CAP', false, '12/08/1996', '', 1, 0, 4, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (45, 'CLAUDIO JEAN DA SILVA PIRES', 'CAP', false, '01/10/1999', '', 0, 0, 0, 1, 1, 15);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (46, 'ANTÔNIO ARAÚJO MESQUITA FILHO', 'CAP', true, '01/08/1993', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (47, 'ANDERSON AUGUSTO CAVALCANTI BATISTA', 'CAP', false, '15/05/1996', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (48, 'URSULLA PRISCYLLA RABELO', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (49, 'IURE DA SILVA CUNHA', 'CAP', false, '01/03/1994', '', 0, 0, 0, 0, 11, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (50, 'ALECIO DE SOUSA LEMOS', 'CAP', false, '01/10/1999', '', 0, 0, 0, 5, 6, 2);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (51, 'ADILSON ARAUJO LIMA', 'CAP', false, '01/10/1999', '', 2, 8, 26, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (52, 'JULIO EMANUEL DANTAS DE MOURA', 'CAP', false, '01/10/1999', '', 3, 2, 7, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (53, 'CLEBER CARVALHO DOS ANJOS', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (54, 'ANA PAULA MARQUES MOURA DA CRUZ', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (55, 'SAULO JOAQUIM NEIVA', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (56, 'FABIANO AUGUSTO DE SOUZA MOREIRA', 'CAP', true, '01/10/1999', '', 0, 0, 0, 1, 5, 6);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (57, 'RONALDO RODRIGUES DA SILVA', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (58, 'ALEXANDRE HONORIO DA SILVA', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (59, 'JOAQUIM MANOEL DO NASCIMENTO FILHO', 'CAP', false, '01/08/1996', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (60, 'MOISES LOPES VIEIRA', 'CAP', false, '01/06/1998', '', 3, 4, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (61, 'WAGNER GOMES DA COSTA', 'CAP', false, '15/05/1996', '', 0, 0, 0, 0, 9, 21);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (62, 'ADERIVALDO MARTINS CARDOSO', 'CAP', true, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (63, 'WENDERSON RODRIGUES RAMOS', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (64, 'LEANDRO GONÇALVES DE SOUZA', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (65, 'VALTENCIR DAS CHAGAS SILVA', 'CAP', false, '15/04/1991', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (66, 'JADSON ALVES BAIÃO SOUSA', 'CAP', false, '01/10/1999', '', 0, 0, 0, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (67, 'CLEBSON NOGUEIRA DE OLIVEIRA', 'CAP', false, '01/04/2003', '', 6, 0, 5, 0, 0, 0);
insert into officers (id, name, rank, agregado, entry_date, promotion_date, ffaa_years, ffaa_months, ffaa_days, civil_years, civil_months, civil_days) values (68, 'THENYSON DA SILVA BISPO', 'CAP', false, '10/03/1997', '', 0, 0, 0, 0, 8, 23);