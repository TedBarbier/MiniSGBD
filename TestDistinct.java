public class TestDistinct {

    public static void main(String[] args) {
        // Create a table with 2 columns
        TableMemoire tm = new TableMemoire(2);

        // Add tuples with duplicates
        // (1, 2)
        Tuple t1 = new Tuple(2);
        t1.val[0] = 1;
        t1.val[1] = 2;
        tm.valeurs.add(t1);

        // (3, 4)
        Tuple t2 = new Tuple(2);
        t2.val[0] = 3;
        t2.val[1] = 4;
        tm.valeurs.add(t2);

        // (1, 2) - Duplicate
        Tuple t3 = new Tuple(2);
        t3.val[0] = 1;
        t3.val[1] = 2;
        tm.valeurs.add(t3);

        // (5, 6)
        Tuple t4 = new Tuple(2);
        t4.val[0] = 5;
        t4.val[1] = 6;
        tm.valeurs.add(t4);

        // (3, 4) - Duplicate
        Tuple t5 = new Tuple(2);
        t5.val[0] = 3;
        t5.val[1] = 4;
        tm.valeurs.add(t5);

        System.out.println("Original Table:");
        for (Tuple t : tm.valeurs) {
            System.out.println(t);
        }

        // Setup operators
        FullScanTableMemoire scan = new FullScanTableMemoire(tm);
        Distinct distinct = new Distinct(scan);

        System.out.println("\nDistinct Output:");
        distinct.open();
        Tuple res;
        while ((res = distinct.next()) != null) {
            System.out.println(res);
        }
        distinct.close();
    }
}
