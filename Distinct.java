import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;

public class Distinct extends Instrumentation implements Operateur {

    private Operateur in;
    private ArrayList<Tuple> sortedTuples;
    private Iterator<Tuple> iterator;
    private Tuple lastReturned;

    public Distinct(Operateur _in) {
        super("Distinct" + Instrumentation.number++);
        this.in = _in;
        this.sortedTuples = new ArrayList<>();
        this.lastReturned = null;
    }

    @Override
    public void open() {
        this.start();
        this.in.open();
        this.tuplesProduits = 0;
        this.memoire = 0;

        Tuple t;
        while ((t = this.in.next()) != null) {
            this.sortedTuples.add(t);
        }

        Collections.sort(this.sortedTuples, new Comparator<Tuple>() {
            @Override
            public int compare(Tuple t1, Tuple t2) {
                if (t1.size != t2.size) {
                    return t1.size - t2.size;
                }
                for (int i = 0; i < t1.size; i++) {
                    if (t1.val[i] != t2.val[i]) {
                        return t1.val[i] - t2.val[i];
                    }
                }
                return 0;
            }
        });

        this.iterator = this.sortedTuples.iterator();
        this.lastReturned = null;
        this.stop();
    }

    @Override
    public Tuple next() {
        this.start();
        while (this.iterator.hasNext()) {
            Tuple current = this.iterator.next();

            boolean isDuplicate = false;
            if (this.lastReturned != null) {
                // Compare current with lastReturned
                if (current.size == lastReturned.size) {
                    boolean equal = true;
                    for (int i = 0; i < current.size; i++) {
                        if (current.val[i] != lastReturned.val[i]) {
                            equal = false;
                            break;
                        }
                    }
                    if (equal) {
                        isDuplicate = true;
                    }
                }
            }

            if (!isDuplicate) {
                this.lastReturned = current;
                this.produit(current);
                this.stop();
                return current;
            }
        }

        this.stop();
        return null;
    }

    @Override
    public void close() {
        this.in.close();
    }
}
