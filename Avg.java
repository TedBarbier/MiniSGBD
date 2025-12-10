
public class Avg extends Instrumentation implements Operateur {

    private int col;
    private Operateur in; 
    private Tuple tempValAvg;
    private int count;

    public Avg(Operateur _in, int _col) {
        super("AVG" + Instrumentation.number++);
        this.start();
        this.col = _col;
        this.in = _in;
        this.tempValAvg = null;
        this.stop();
    }

    @Override
    public void open() {
        this.start();
        this.in.open();
        this.tuplesProduits = 0;
        this.memoire = 0;
        Tuple temp = null;
        this.tempValAvg = this.in.next();
        if (this.tempValAvg != null) {
            this.count = 1;
            while ((temp = this.in.next()) != null) {
                count++;
                this.tempValAvg.val[this.col] += temp.val[this.col];
            }
            this.tempValAvg.val[this.col] /= count;
        }
        this.stop();
    }

    @Override
    public Tuple next() {
        this.start();
        if (this.tempValAvg == null) {
            this.stop();
            return null;
        } else {
            Tuple ret = new Tuple(1);
            ret.val[0] = this.tempValAvg.val[this.col];
            this.tempValAvg = null;
            this.produit(ret);
            this.stop();
            return ret;
        }
    }

    @Override
    public void close() {
        this.in.close();
    }

}
