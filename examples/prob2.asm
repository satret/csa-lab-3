section .data
    fib1: word 1
    fib2: word 2
    temp: word 0
    sum: word 2
    limit: word 4000000

section .text
    start:
        cmp fib2, limit
        jg finish

        ld fib1
        ld fib2
        add fib1
        st temp

        ld fib2
        st fib1
        ld temp
        st fib2

        mod fib2, #2
        cmp #0
        je add_to_sum
        jmp start

    add_to_sum:
        ld sum
        add fib2
        st sum
        jmp start

    finish:
        hlt
