'''Alright so I'm a new flavor of fucked. I need to write THREE fucking AI programs right off the bat. in a Language I dont even know...so let the smoldering fire begin'''

'''
Assignment 1 (non bonus):

Write a Hill-Climbing algorithm pseudo
-------------------------------------
From wikipedia
{
hill-climbing algorithm: Discrete Space Climbing Hill is
1.    currentNode:= startNode
2.    loop do
        L := NEIGHBORS(currentNode)
        nextEval := -INF
        nextNode := NULL
        for all x in L do
            if EVAL(x) > nextEval then
                nextNode := x
                nextEval := EVAL(x)
        if nextEval <= EVAL(currentNode) then
            // Return current node since no better neighbors exist
            return currentNode
        currentNode := nextNode
}

From notes (ch1)
procedure iterated hill-climbing algorithm
PLEASE NOTE ^= equates to SUBSCRIPT for myself.

begin
{
    t <- 0
    repeat
    {
        local <- FALSE
        select a current string v[^=current] at random
        evaluate v[^=current]
        repeat
        {
            select 30 new strings in the neighborhood of v[^=current] by flipping single bits of v[^=current]

            select the string v[^=neighbor] from the set of new strings with the largest value of objective function f

            if f( v[^=current] ) < f( v[^=neighbor] )
            {
                then v[^=current] <- v[^=neighbor]
            }
        }
    }
    until t = MAX

}









Write a Simmulated-Annealing algorithm pseudo
-----------------------------------







'''

