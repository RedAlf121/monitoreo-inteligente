talla(1,1).
talla(2,1).
talla(3,1).
talla(4,1).

talla(X,Y) :-
    X > 4,
    X1 is X - 1,
    talla(X1, Y1),
    Y is Y1 + X.
