-- AlterTable
ALTER TABLE "Assets" ADD COLUMN     "recordStatus" TEXT NOT NULL DEFAULT 'created';

-- AlterTable
ALTER TABLE "Users" ADD COLUMN     "recordStatus" TEXT NOT NULL DEFAULT 'created';

-- CreateTable
CREATE TABLE "AssetIsSell" (
    "id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "asssetId" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "recordStatus" TEXT NOT NULL DEFAULT 'created',

    CONSTRAINT "AssetIsSell_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AssetIsRequestBuy" (
    "id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "asssetId" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "recordStatus" TEXT NOT NULL DEFAULT 'created',

    CONSTRAINT "AssetIsRequestBuy_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Transaction" (
    "id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "senderUserId" TEXT NOT NULL,
    "receiverUserId" TEXT NOT NULL,
    "blockchainTransactionId" TEXT NOT NULL,
    "sender" TEXT NOT NULL,
    "receiver" TEXT NOT NULL,
    "metadata" JSONB NOT NULL,
    "recordStatus" TEXT NOT NULL DEFAULT 'created',

    CONSTRAINT "Transaction_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "AssetIsSell_asssetId_key" ON "AssetIsSell"("asssetId");

-- AddForeignKey
ALTER TABLE "AssetIsSell" ADD CONSTRAINT "AssetIsSell_asssetId_fkey" FOREIGN KEY ("asssetId") REFERENCES "Assets"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AssetIsSell" ADD CONSTRAINT "AssetIsSell_userId_fkey" FOREIGN KEY ("userId") REFERENCES "Users"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AssetIsRequestBuy" ADD CONSTRAINT "AssetIsRequestBuy_asssetId_fkey" FOREIGN KEY ("asssetId") REFERENCES "Assets"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AssetIsRequestBuy" ADD CONSTRAINT "AssetIsRequestBuy_userId_fkey" FOREIGN KEY ("userId") REFERENCES "Users"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
